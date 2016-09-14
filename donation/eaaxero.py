# pip install PyCrypto PyXero cryptography
from datetime import date, timedelta
import hashlib

from collections import defaultdict
from xero import Xero
from xero.auth import PrivateCredentials

from django.conf import settings

from models import BankTransaction

credentials = PrivateCredentials(settings.XERO_CONSUMER_KEY, settings.XERO_RSA_KEY)
xero = Xero(credentials)


def import_bank_transactions():
    to_date = date.today()
    from_date = to_date - timedelta(settings.XERO_DAYS_TO_IMPORT)

    passed_params = {
        "fromDate": str(from_date),
        "toDate": str(to_date),

        # Note: you can look up the bankAccountIDs by using the xero.accounts endpoint and filtering account number.
        "bankAccountID": settings.XERO_ACCOUNT_ID_FOR_INCOMING_DONATIONS

        # This was our old Westpac account.
        # TODO maybe do a one-time import of donations from this account if we ever do things like
        # look at how much a donor has donated in total.
        # "bankAccountID": u'9bc4450a-ed06-4049-abbc-03e723581d18',
    }

    bank_transactions = xero.reports.get('BankStatement', params=passed_params)[0]
    xero_headers = [cell[u'Value'] for cell in bank_transactions['Rows'][0]['Cells']]

    rows_seen = defaultdict(int)
    for row in bank_transactions['Rows'][1]['Rows']:
        data = dict(zip(xero_headers, [cell[u'Value'] for cell in row[u'Cells']]))

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

        try:
            BankTransaction.objects.get(unique_id=unique_id)
        except BankTransaction.DoesNotExist:
            BankTransaction.objects.create(date=bank_statement_date,
                                           bank_statement_text=bank_statement_text,
                                           amount=amount,
                                           unique_id=unique_id)
