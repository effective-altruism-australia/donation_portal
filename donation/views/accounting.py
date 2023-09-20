from __future__ import absolute_import

from datetime import date

import arrow
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum, Min, F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from raven.contrib.django.raven_compat.models import client

from donation.forms import DateRangeSelector
from donation.models import XeroReconciledDate, Account, Donation, PartnerCharity, BankTransaction


def total_donations_for_partner(start_date, end_date, partner, payment_method=None, after_fees=False, card_type=None):
    # We use the Donation view because I've thought carefully about the time zone handling for that.
    # If you were to use the PinTransaction model directly to calculate total credit card donations,
    # you need to think more carefully about time zones.
    filters = {
        'date__gte': start_date,
        'date__lt': arrow.get(end_date).shift(days=1).date(),
        'components__pledge_component__partner_charity': partner,
    }
    id_field = "id"
    if payment_method == 'Stripe':
        filters['stripe_transaction_id__isnull'] = False
        id_field = "stripe_transaction_id"
    elif payment_method == 'Pin':
        filters['pin_transaction_id__isnull'] = False
        id_field = "pin_transaction_id"
    elif payment_method == 'Bank transfer':
        filters['bank_transaction_id__isnull'] = False
        id_field = "bank_transaction_id"
    d = Donation.objects.filter(**filters)
    if not d.exists():
        return 0
    earliest_id = d.earliest(id_field).id
    filters[id_field + "__gte"] = earliest_id
    latest_id = d.latest(id_field).id
    filters[id_field + "__lte"] = latest_id

    return Donation.objects \
               .filter(**filters) \
               .annotate(amount_maybe_less_fees=F('components__amount') - (F('components__fees') if after_fees else 0)) \
               .aggregate(Sum('amount_maybe_less_fees'))['amount_maybe_less_fees__sum'] or 0


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

    # Dev instances may not have a xero_reconciled_date
    xero_reconciled_date = xero_reconciled_date or date(2015, 12, 31)

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

    totals = {partner.name: float(Account.objects
                                  .filter(date__gte=xero_start_date, date__lte=xero_end_date,
                                          name=partner.xero_account_name)
                                  .aggregate(Sum('amount'))['amount__sum'] or 0) +
                            float(total_donations_for_partner(django_start_date, django_end_date, partner))
              for partner in PartnerCharity.objects.all().order_by('name')}

    unknown_total = BankTransaction.objects.filter(date__gte=django_start_date, date__lte=django_end_date,
                                                   do_not_reconcile=False, pledge__isnull=True, amount__gte=0) \
        .aggregate(Sum('amount'))['amount__sum']
    if unknown_total:
        totals['Unknown as yet'] = float(unknown_total)

    # Temporary hack - these will be included in the partners soon.
    # Add donations present in xero but not in the partners
    for account_description, account_name in [
        ("TBD - for partner charity of our choice",
         "Donations received - for partner charity of our choice (250-PARTNE)"),
        ("Unrestricted", "Donations received - Unrestricted (251)")
    ]:
        account_total = (Account.objects
                         .filter(date__gte=xero_start_date, date__lte=xero_end_date,
                                 name=account_name)
                         .aggregate(Sum('amount'))['amount__sum'] or 0)
        if account_total:
            totals[account_description] = float(account_total)

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
def _accounting_reconciliation(request, is_eaae):
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

    totals = {partner.name:
                  {'bank': total_donations_for_partner(start, end, partner, payment_method='Bank transfer'),
                   'pin_payments': total_donations_for_partner(start, end, partner, payment_method='Pin'),
                   'pin_payments_after_fees': total_donations_for_partner(start, end, partner,
                                                                         payment_method='Pin', after_fees=True),
                   'stripe': total_donations_for_partner(start, end, partner, payment_method='Stripe'),
                   'stripe_after_fees': total_donations_for_partner(start, end, partner, payment_method='Stripe', after_fees=True),
                   'total': total_donations_for_partner(start, end, partner)}
              for partner in PartnerCharity.objects.filter(is_eaae=is_eaae).order_by('name')}

    grand_total = {kind: sum(total[kind] for total in totals.values()) for kind in ('bank', 'pin_payments',
                                                                                    'pin_payments_after_fees',
                                                                                    'stripe',
                                                                                    'stripe_after_fees', 'total')}

    # This shouldn't/can't happen but it will mess up the reconciliation so let's check.
    qs = BankTransaction.objects.filter(pledge__isnull=False, do_not_reconcile=True, is_eaae=is_eaae)
    if qs.exists():
        message = "Error: transaction reconciled to pledge and also marked 'Do not reconcile', please check " \
                  "bank transactions with id: %s" % ', '.join(qs.values_list('id', flat=True))
        client.captureException("Error: transaction reconciled to pledge and also marked 'Do not reconcile'")
        return HttpResponse(message)

    exceptions = BankTransaction.objects.filter(date__gte=start, date__lte=end, is_eaae=is_eaae).exclude(pledge__isnull=False).order_by(
        'date')

    return render(request, 'reconciliation.html', {'form': form,
                                                   'totals': sorted(totals.iteritems()),
                                                   'grand_total': grand_total,
                                                   'exceptions': exceptions})

@login_required()
def accounting_reconciliation(request):
    return _accounting_reconciliation(request, False)

@login_required()
def accounting_reconciliation_eaae(request):
    return _accounting_reconciliation(request, True)