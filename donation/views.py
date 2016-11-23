from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.urlresolvers import reverse

from .forms import TransitionalDonationsFileUploadForm, DateRangeSelector
from .models import BankTransaction, PartnerCharity


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


@login_required()
def accounting_reconciliation(request):
    if request.method == 'POST':
        form = DateRangeSelector(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('accounting_reconciliation'))
    else:
        form = DateRangeSelector()

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

    exceptions = BankTransaction.objects.filter(date__gte=start, date__lte=end).exclude(pledge__isnull=False).order_by('date')

    return render(request, 'reconciliation.html', {'form': form,
                                                   'totals': sorted(totals.iteritems()),
                                                   'grand_total': sum(totals.values()),
                                                   'exceptions': exceptions})
