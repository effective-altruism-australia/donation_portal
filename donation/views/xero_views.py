from django.http import HttpResponseRedirect
from django.core.cache import caches

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes
from django.conf import settings

def start_xero_auth_view(request):
    # Get client_id, client_secret from config file or settings then
    credentials = OAuth2Credentials(
        settings.XERO_CLIENT_ID, settings.XERO_CLIENT_SECRET, callback_uri="https://donations.effectivealtruism.org.au/process_callback",
        scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS,
                XeroScopes.ACCOUNTING_TRANSACTIONS]
    )
    authorization_url = credentials.generate_url()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponseRedirect(authorization_url)


def process_callback_view(request):
    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    print(request.META)
    auth_secret = request.META['RAW_URI']
    credentials.verify(auth_secret)
    credentials.set_default_tenant()
    caches['default'].set('xero_creds', credentials.state)

    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    if credentials.expired():
        credentials.refresh()
        caches['default'].set('xero_creds', credentials.state)
    xero = Xero(credentials)
