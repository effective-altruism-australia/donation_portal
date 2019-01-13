"""donation_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from donation.views.accounting import accounting_reconciliation, donation_counter
from donation.views.export import render_export_page, download_spreadsheet, download_full_spreadsheet
from donation.views.form_data import PartnerCharityView, ReferralSourceView
from donation.views.pledge import PledgeView, download_receipt, PledgeViewOld, PledgeJS
from datetime import date

import arrow
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum, Min, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from donation.forms import DateRangeSelector
from donation.models import XeroReconciledDate, Account, Donation, PartnerCharity, BankTransaction
from django.utils.safestring import mark_safe

def asdf(request):
    donation = Donation.objects.get(id=1000004)
    pledge = donation.pledge
    assert pledge.is_gift, 'Expected the pledge to be marked as a gift'
    assert not pledge.gift_message_sent, 'Gift message has already been sent'
    # charities = []
    # for component in donation.components.all():
    #     charities.append(
    #         {
    #             'partner': component.pledge_component.partner_charity,
    #             'impact': component.impact_str(),
    #             'component': component
    #         }
    #     )
    context = {'pledge': pledge,
               'donation': donation,
               'personal_message': mark_safe(pledge.gift_personal_message)
               }
    return render(request, 'gift_message.html', context)

urlpatterns = [
    url(r'^test', asdf, name='asdf-sadfd'),

    # Accounting
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounting_reconciliation', accounting_reconciliation, name='accounting-reconciliation'),
    url(r'^secret_donation_counter', donation_counter, name='donation-counter'),
    # Data export
    url(r'^export', render_export_page, name='export-page'),
    url(r'^download_full_spreadsheet', download_full_spreadsheet, name='download-full-spreadsheet'),
    url(r'^download_spreadsheet', download_spreadsheet, name='download-spreadsheet'),
    # Donations
    # url(r'^pledge/([0-9])/$', pledge, name='pledge')
    url(r'^pledge.js', PledgeJS.as_view(), name='pledge-js'),
    url(r'^pledge_new/', PledgeView.as_view(), name='pledge-new'),
    url(r'^pledge/', PledgeViewOld.as_view(), name='pledge'),

    url(r'^receipt/(?P<pk>[0-9]+)/(?P<secret>[a-zA-Z0-9]+)', download_receipt, name='download-receipt'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    url(r'^partner_charities', PartnerCharityView.as_view(), name='partner-charities'),
    url(r'^referral_sources', ReferralSourceView.as_view(), name='referral-sources'),

]

urlpatterns += staticfiles_urlpatterns()

urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
