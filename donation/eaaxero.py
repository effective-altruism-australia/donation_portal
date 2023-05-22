# pip install PyCrypto PyXero cryptography
from datetime import date, timedelta
from decimal import Decimal
import hashlib
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from xero import Xero
from xero.exceptions import XeroNotFound
from django.core.cache import caches
from django.conf import settings

from .models import BankTransaction, Account
from xero.constants import XeroScopes
from xero.auth import OAuth2Credentials
from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes


def xero(tenant):
    cred_state = caches['default'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    if credentials.expired():
        credentials.refresh()
        caches['default'].set('xero_creds', credentials.state)
    credentials.tenant_id = settings.TENANT_IDS.get(tenant)
    return Xero(credentials)


def xero_report_to_iterator(xero_report):
    # Iterate through a report from xero. Each row is returned as a dictionary.
    # Note that this doesn't give us the whole report, but it's enough for the
    # the reports that we need.
    headers = [cell[u'Value'] for cell in xero_report[0]['Rows'][0]['Cells']]
    for row in xero_report[0]['Rows'][1]['Rows']:
        yield dict(zip(headers, [cell[u'Value'] for cell in row[u'Cells']]))


def import_bank_transactions(manual=False, tenant = 'eaa'):
    to_date = date.today()
    from_date = to_date - timedelta(settings.XERO_DAYS_TO_IMPORT)
    import_bank_transactions_from_account(settings.XERO_INCOMING_ACCOUNT_ID_DICT.get(tenant), from_date, to_date, manual, tenant)


def import_bank_transactions_from_account(bank_account_id, from_date, to_date, manual, tenant = "eaa"):
    passed_params = {
        "fromDate": str(from_date),
        "toDate": str(to_date),
        # Note: you can look up the bankAccountIDs by using the xero.accounts endpoint and filtering account number.
        "bankAccountID": bank_account_id
    }

    rows_seen = defaultdict(int)
    try:
        bank_transactions = xero(tenant).reports.get('BankStatement', params=passed_params)
    except XeroNotFound:
        if manual:
            # If user invoked this function manually, raise the exception.
            raise
        else:
            # But probably xero is temporarily down. We'll get the transactions next time.
            return

    for data in xero_report_to_iterator(bank_transactions):
        # Omit "Opening Balance" and "Closing Balance"
        if data[u'Description'] in [u'Opening Balance', u'Closing Balance']:
            continue

        bank_statement_date = data[u'Date']
        bank_statement_text = data[u'Reference']
        amount = data[u'Amount']

        # Create a unique id to simplify import. Note that it's more robust to not include the balance in the hash
        # since then if there's a error, e.g., a missing transactions, which does happen in xero from time to time,
        # then fixing it will not cause all later unique id's to change.
        unique_id = hashlib.md5("x".join([bank_statement_text, str(bank_statement_date), amount])).hexdigest()

        # A donor may make two or more identical donations on the same day. Deal with this:
        rows_seen[unique_id] += 1
        if rows_seen[unique_id] > 1:
            unique_id = hashlib.md5(unique_id + str(rows_seen[unique_id])).hexdigest()
        
        if "STRIPE EFFECTIVE ALT" in bank_statement_text:
            continue

        try:
            BankTransaction.objects.get(unique_id=unique_id)
        except BankTransaction.DoesNotExist:
            BankTransaction.objects.create(date=bank_statement_date,
                                           bank_statement_text=bank_statement_text,
                                           amount=amount,
                                           unique_id=unique_id,
                                           bank_account_id=bank_account_id,
                                           is_eaae=tenant=="eaae")


def to_decimal(s):
    return Decimal(s) if s else Decimal(0)


def import_trial_balance(org):
    balance_date = date(2016, 1, 31)
    while balance_date < date.today():
        trial_balance = xero(org).reports.get('TrialBalance', params={u'Date': balance_date})

        for row in xero_report_to_iterator(trial_balance):
            try:
                account = Account.objects.get(date=balance_date, name=row[u'Account'])
            except Account.DoesNotExist:
                account = Account(date=balance_date, name=row[u'Account'])
            account.amount = to_decimal(row[u'Credit']) - to_decimal(row[u'Debit'])
            account.ytd_amount = to_decimal(row[u'YTD Credit']) - to_decimal(row[u'YTD Debit'])
            account.save()

        balance_date += relativedelta(days=1)
        balance_date += relativedelta(months=1)
        balance_date -= relativedelta(days=1)
