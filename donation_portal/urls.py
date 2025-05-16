from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from donation.views.accounting import accounting_reconciliation, donation_counter, accounting_reconciliation_eaae
from donation.views.export import render_export_page, download_spreadsheet, download_full_spreadsheet
from donation.views.form_data import PartnerCharityView, ReferralSourceView
from donation.views.pledge import stripe_webhooks_eaae, stripe_billing_portal_eaae, PledgeView, download_receipt, stripe_webhooks, stripe_billing_portal
from donation.views.impact_calculator import ImpactCalculator
from donation.views.xero_views import process_callback_view, start_xero_auth_view

urlpatterns = [
    # Accounting
    path('admin/', admin.site.urls),
    path("accounting_reconciliation/", accounting_reconciliation, name="accounting-reconciliation"),
    path("eaae_accounting_reconciliation/", accounting_reconciliation_eaae, name="accounting-reconciliation-eaae"),
    path("impact/", ImpactCalculator.as_view(), name="impact"),
    path("secret_donation_counter/", donation_counter, name="donation-counter"),
    # Data export
    path("export/", render_export_page, name="export-page"),
    path("download_full_spreadsheet/", download_full_spreadsheet, name="download-full-spreadsheet"),
    path("download_spreadsheet/", download_spreadsheet, name="download-spreadsheet"),
    # Donations
    path("pledge_new/", PledgeView.as_view(), name="pledge-new"),

    path("receipt/<int:pk>/<slug:secret>/", download_receipt, name="download-receipt"),
    path("paypal/", include("paypal.standard.ipn.urls")),

    path("partner_charities/", PartnerCharityView.as_view(), name="partner-charities"),
    path("referral_sources/", ReferralSourceView.as_view(), name="referral-sources"),
    
    path("stripe-webhooks-eaae/", stripe_webhooks_eaae, name="stripe-webhooks-eaae"),

    path("stripe-webhooks/", stripe_webhooks, name="stripe-webhooks"),


    path("donor-portal/<path:customer_id>/", stripe_billing_portal, name="donor-portal-eaa"),
    
    path("donor-portal-eaae/<path:customer_id>/", stripe_billing_portal_eaae, name="donor-portal-eaae"),
    
    path("process_callback/", process_callback_view, name="process-callback"),
    path("xero_auth/", start_xero_auth_view, name="start-auth"),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns.append(path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}))

# Only include the debug toolbar URLs if DEBUG is True
if settings.DEBUG and settings.ENABLE_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()