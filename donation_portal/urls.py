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

from donation.views.accounting import accounting_reconciliation, donation_counter, accounting_reconciliation_eaae
from donation.views.export import render_export_page, download_spreadsheet, download_full_spreadsheet
from donation.views.form_data import PartnerCharityView, ReferralSourceView
from donation.views.pledge import stripe_webhooks_eaae, stripe_billing_portal_eaae, PledgeView, download_receipt, PledgeJS, stripe_webhooks, stripe_billing_portal
from donation.views.impact_calculator import ImpactCalculator
from donation.views.xero_views import process_callback_view, start_xero_auth_view

urlpatterns = [
    # Accounting
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounting_reconciliation', accounting_reconciliation, name='accounting-reconciliation'),
    url(r'^eaae_accounting_reconciliation', accounting_reconciliation_eaae, name='accounting-reconciliation-eaae'),
    url(r'^impact', ImpactCalculator.as_view(), name='impact'),
    url(r'^secret_donation_counter', donation_counter, name='donation-counter'),
    # Data export
    url(r'^export', render_export_page, name='export-page'),
    url(r'^download_full_spreadsheet', download_full_spreadsheet, name='download-full-spreadsheet'),
    url(r'^download_spreadsheet', download_spreadsheet, name='download-spreadsheet'),
    # Donations
    # url(r'^pledge/([0-9])/$', pledge, name='pledge')
    url(r'^pledge.js', PledgeJS.as_view(), name='pledge-js'),
    url(r'^pledge_new/', PledgeView.as_view(), name='pledge-new'),

    url(r'^receipt/(?P<pk>[0-9]+)/(?P<secret>[a-zA-Z0-9]+)', download_receipt, name='download-receipt'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    url(r'^partner_charities', PartnerCharityView.as_view(), name='partner-charities'),
    url(r'^referral_sources', ReferralSourceView.as_view(), name='referral-sources'),
    
    url(r'^stripe-webhooks-eaae', stripe_webhooks_eaae, name='stripe-webhooks-eaae'),

    url(r'^stripe-webhooks', stripe_webhooks, name='stripe-webhooks'),


    url(r'^donor-portal/(?P<customer_id>.*)', stripe_billing_portal, name='donor-portal-eaa'),
    
    url(r'^donor-portal-eaae/(?P<customer_id>.*)', stripe_billing_portal_eaae, name='donor-portal-eaae'),
    
    url(r'^process_callback', process_callback_view, name='process-callback'),
    url(r'^xero_auth', start_xero_auth_view, name='start-auth'),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
