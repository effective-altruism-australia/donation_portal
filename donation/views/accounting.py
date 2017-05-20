from __future__ import absolute_import

from datetime import date

import arrow
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum, Min
from django.http import HttpResponseRedirect
from django.shortcuts import render

from donation.forms import DateRangeSelector
from donation.models import XeroReconciledDate, Account, Donation, PartnerCharity, BankTransaction, PinTransaction


def total_donations_for_partner(DonationModel, start_date, end_date, partner):
    return DonationModel.objects \
               .filter(date__gte=start_date, date__lte=end_date, pledge__recipient_org=partner) \
               .aggregate(Sum('amount'))['amount__sum'] or 0


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

    totals = {partner.name: (Account.objects
                             .filter(date__gte=xero_start_date, date__lte=xero_end_date, name=partner.xero_account_name)
                             .aggregate(Sum('amount'))['amount__sum'] or 0) +
                            total_donations_for_partner(Donation, django_start_date, django_end_date, partner)
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

    totals = {partner.name:
                  {'bank': total_donations_for_partner(BankTransaction, start, end, partner),
                   'credit_card': total_donations_for_partner(PinTransaction, start, end, partner),
                   'total': total_donations_for_partner(Donation, start, end, partner)}
              for partner in PartnerCharity.objects.all().order_by('name')}

    grand_total = {kind: sum(total[kind] for total in totals.values()) for kind in ('bank', 'credit_card', 'total')}

    # This shouldn't/can't happen but it will mess up the reconciliation so let's check.
    if BankTransaction.objects.filter(pledge__isnull=False, do_not_reconcile=True).exists():
        raise Exception("Error: transaction reconciled to pledge and also marked 'Do not reconcile'")

    exceptions = BankTransaction.objects.filter(date__gte=start, date__lte=end).exclude(pledge__isnull=False).order_by(
        'date')

    return render(request, 'reconciliation.html', {'form': form,
                                                   'totals': sorted(totals.iteritems()),
                                                   'grand_total': grand_total,
                                                   'exceptions': exceptions})
