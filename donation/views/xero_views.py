from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import caches
from django.shortcuts import render

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes
from django.conf import settings

def start_xero_auth_view(request):
    # Get client_id, client_secret from config file or settings then
    credentials = OAuth2Credentials(
        settings.XERO_CLIENT_ID, settings.XERO_CLIENT_SECRET, callback_uri="https://donations.effectivealtruism.org.au/process_callback",
        scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS, XeroScopes.ACCOUNTING_REPORTS_READ,
                XeroScopes.ACCOUNTING_TRANSACTIONS, "accounting.reports.bankstatement.read"]
    )
    authorization_url = credentials.generate_url()
    caches['default'].set('xero_creds', credentials.state)
    return HttpResponseRedirect(authorization_url)


def process_callback_view(request):
    context = {
        'success': False,
        'error_message': None,
        'tenant_info': None
    }
    
    try:
        cred_state = caches['default'].get('xero_creds')
        if not cred_state:
            context['error_message'] = 'No authentication state found. Please restart the login process.'
            return render(request, 'xero_callback_status.html', context)
        
        credentials = OAuth2Credentials(**cred_state)
        auth_secret = request.build_absolute_uri()
        credentials.verify(auth_secret)
        credentials.set_default_tenant()
        caches['default'].set('xero_creds', credentials.state)
        
        # Get tenant information for display
        try:
            xero = Xero(credentials)
            organisations = xero.organisations.all()
            if organisations:
                context['tenant_info'] = {
                    'name': organisations[0]['Name'],
                    'short_code': organisations[0]['ShortCode'],
                    'country_code': organisations[0]['CountryCode']
                }
        except Exception as e:
            # Even if we can't get org info, the login might have worked
            context['tenant_info'] = {'name': 'Organization details unavailable'}
        
        context['success'] = True
        
    except Exception as e:
        context['error_message'] = f'Authentication failed: {str(e)}'
    
    return render(request, 'xero_callback_status.html', context)
