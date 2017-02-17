import xlsxwriter
from datetime import datetime, date
import os
import arrow

from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max, Min
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import View, CreateView
from django.views.decorators.clickjacking import xframe_options_exempt

from .forms import TransitionalDonationsFileUploadForm, DateRangeSelector, PledgeForm
from .models import BankTransaction, PartnerCharity, XeroReconciledDate, Account, PinTransaction, Receipt, RecurringFrequency
from paypal.standard.forms import PayPalPaymentsForm


@login_required()
def upload_donations_file(request):
    if request.method == 'POST':
        form = TransitionalDonationsFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/admin/donation/pledge/')
    else:
        form = TransitionalDonationsFileUploadForm()
    return render(request, 'transitional_upload_form.html', {'form': form})


def donation_counter(request):
    if request.method == 'POST':
        form = DateRangeSelector(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('donation-counter'))
    else:
        form = DateRangeSelector()

    # There's gotta be a better way to do this
    if hasattr(form, 'cleaned_data'):
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        start = form.fields['start'].initial
        end = form.fields['end'].initial

    # Usually the accounting won't be quite up to date. Use Xero for transactions before xero_up_to_date_until_date
    # and bank transactions for after
    xero_reconciled_date = XeroReconciledDate.objects.all().aggregate(Max('date'))['date__max']

    xero_start_date = start
    xero_end_date = min(xero_reconciled_date, end)
    django_start_date = max(arrow.get(xero_reconciled_date).replace(days=1).date(), start)
    django_end_date = end

    # This will only give correct answers if you specify whole months during the period we take data from xero.
    # We don't do the accounting in a way that provides daily data so this is not possible to improve.
    error_message = ''
    if (xero_start_date <= xero_reconciled_date and xero_start_date.day != 1) or \
                    arrow.get(xero_end_date).replace(days=1).date().day != 1:
        error_message = "You must specify complete months for this period because of the way we do the accounting" + \
                        " in xero. Please set the start date to the start of a month and the end date to the end of" + \
                        " a month."

    totals = {partner.name: (Account.objects
        .filter(date__gte=xero_start_date, date__lte=xero_end_date, name=partner.xero_account_name)
        .aggregate(Sum('amount'))['amount__sum'] or 0) +
                            (BankTransaction.objects
        .filter(date__gte=django_start_date, date__lte=django_end_date, pledge__recipient_org=partner)
        .aggregate(Sum('amount'))['amount__sum'] or 0)
              for partner in PartnerCharity.objects.all().order_by('name')}

    unknown_total = BankTransaction.objects.filter(date__gte=django_start_date, date__lte=django_end_date,
                                                   do_not_reconcile=False, pledge__isnull=True, amount__gte=0) \
                                    .aggregate(Sum('amount'))['amount__sum']
    if unknown_total:
        totals['Unknown as yet'] = unknown_total

    receipt_date = BankTransaction.objects.filter(do_not_reconcile=False, pledge__isnull=True, amount__gte=0) \
                                  .aggregate(Min('date'))['date__min']

    return render(request, 'donation_counter.html', {'form': form,
                                                     'totals': sorted(totals.iteritems()),
                                                     'grand_total': sum(filter(None, totals.values())),
                                                     'error_message': error_message,
                                                     'xero_reconciled_date': xero_reconciled_date,
                                                     'receipt_date': receipt_date,
                                                     })


@login_required()
def accounting_reconciliation(request):
    if request.method == 'POST':
        form = DateRangeSelector(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('accounting-reconciliation'))
    else:
        form = DateRangeSelector(last_month=True)

    # There's gotta be a better way to do this
    if hasattr(form, 'cleaned_data'):
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
    else:
        start = form.fields['start'].initial
        end = form.fields['end'].initial

    totals = {partner.name: BankTransaction.objects
        .filter(date__gte=start, date__lte=end, pledge__recipient_org=partner)
        .aggregate(Sum('amount'))['amount__sum']
              for partner in PartnerCharity.objects.all().order_by('name')}

    # This shouldn't/can't happen but it will mess up the reconciliation so let's check.
    if BankTransaction.objects.filter(pledge__isnull=False, do_not_reconcile=True).exists():
        raise Exception("Error: transaction reconciled to pledge and also marked 'Do not reconcile'")

    exceptions = BankTransaction.objects.filter(date__gte=start, date__lte=end).exclude(pledge__isnull=False).order_by(
        'date')

    return render(request, 'reconciliation.html', {'form': form,
                                                   'totals': sorted(totals.iteritems()),
                                                   'grand_total': sum(filter(None, totals.values())),
                                                   'exceptions': exceptions})


@login_required()
def download_transactions(request):
    # TODO We don't pass parameters to this function yet.
    # Write some javascript to restrict dates. Maybe easiest to switch out the date widgets for the jQuery UI ones.
    if request.method != 'GET':
        raise Http404

    try:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        start = date(2016, 1, 1)

    try:
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        end = date.today()

    path = os.path.join(settings.MEDIA_ROOT, 'downloads')
    filename = 'EAA donations {0} to {1} downloaded {2}.xlsx'.format(start, end, datetime.now())
    with xlsxwriter.Workbook(os.path.join(path, filename)) as wb:
        ws = wb.add_worksheet()
        date_format = wb.add_format({'num_format': 'dd mmm yyyy'})
        from collections import OrderedDict
        template = OrderedDict([
            ('Date', 'date'),
            ('Amount', 'amount'),
            ('EAA Reference', 'reference'),
            ('First Name', 'pledge__first_name'),
            ('Last Name', 'pledge__last_name'),
            ('Email', 'pledge__email'),
            ('Subscribe to marketing updates', 'pledge__subscribe_to_updates'),
            ('Can publish donation', 'pledge__publish_donation'),
            ('Designation', 'pledge__recipient_org__name')
        ])
        ws.write_row(0, 0, template.keys())
        row = 0
        for bt_row in BankTransaction.objects. \
                filter(date__gte=start, date__lte=end, do_not_reconcile=False). \
                order_by('date'). \
                values_list(*template.values()):
            row += 1
            ws.write_datetime(row, 0, bt_row[0], date_format)
            ws.write_row(row, 1, bt_row[1:])

    response = HttpResponse(open(os.path.join(path, filename)).read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


def download_receipt(request, pk, secret):
    if request.method != 'GET':
        raise Http404
    try:
        receipt = Receipt.objects.get(pk=pk, secret=secret)
    except Receipt.DoesNotExist:
        return HttpResponseRedirect('/pledge')
    response = HttpResponse(open(receipt.pdf_receipt_location).read(),
                            content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EAA_Receipt_{0}.pdf"'.format(receipt.pk)
    return response


# TODO It's weird these are combined since one is JSON and one is not
class PledgeView(View):
    @xframe_options_exempt
    def post(self, request):
        form = PledgeForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            return JsonResponse({
                'error': 'form-error',
                'form_errors': form.errors
            }, status=400)

        pledge = form.instance
        if pledge.recurring:
            pledge.recurring_frequency = RecurringFrequency.MONTHLY
            pledge.save()
        payment_method = request.POST.get('payment_method')
        response_data = {'payment_method': payment_method}

        if int(payment_method) == 1:
            # bank transaction
            pledge.send_bank_transfer_instructions()
            response_data['bank_reference'] = pledge.generate_reference()
            return JsonResponse(response_data)
        elif int(payment_method) == 3:
            transaction = PinTransaction()
            transaction.card_token = request.POST.get('card_token')
            transaction.ip_address = request.POST.get('ip_address')
            transaction.amount = form.cleaned_data['amount']  # Amount in dollars. Define with your own business logic.
            transaction.currency = 'AUD'  # Pin supports AUD and USD. Fees apply for currency conversion.
            transaction.description = 'Donation to Effective Altruism Australia'  # Define with your own business logic
            transaction.email_address = pledge.email
            transaction.pledge = pledge
            transaction.save()
            transaction.process_transaction()  # Typically "Success" or an error message
            if transaction.succeeded:
                response_data['succeeded'] = True
                receipt = transaction.receipt_set.first()
                response_data['receipt_url'] = reverse('download-receipt',
                                                       kwargs={'pk': receipt.pk, 'secret': receipt.secret})
                return JsonResponse(response_data)
            else:
                return JsonResponse({
                    'error': 'pin-error',
                    'pin_response': transaction.pin_response,
                    'pin_response_text': transaction.pin_response_text,
                }, status=400)

    @xframe_options_exempt
    def get(self, request):
        paypal_dict = {
            "business": "placeholder@example.com",
            "amount": "0",
            "item_name": "Donation",
            "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
            "return_url": "https://www.example.com/your-return-location/",
            "cancel_return": "https://www.example.com/your-cancel-location/",
        }
        paypal_form = PayPalPaymentsForm(button_type='donate', initial=paypal_dict)
        form = PledgeForm()

        return render(request, 'pledge.html', {
            'form': form,
            'paypal_form': paypal_form,
            'charity_database_ids': PartnerCharity.get_cached_database_ids(),
            })
