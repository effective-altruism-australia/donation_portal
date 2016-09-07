# pip install PyCrypto PyXero cryptography
from datetime import date, timedelta
import hashlib
import csv
import os
import re
from collections import defaultdict

from xero import Xero
from xero.auth import PrivateCredentials

from models import BankTransaction

# TODO
base_dir = '/share/eaa'


def import_bank_transactions():
    rsa_key = open(os.path.join(base_dir, 'rsa_key.txt')).read()
    consumer_key = open(os.path.join(base_dir, 'consumer_key.txt')).read().strip()
    credentials = PrivateCredentials(consumer_key, rsa_key)
    xero = Xero(credentials)

    to_date = date.today()
    from_date = to_date - timedelta(days=300)

    passed_params = {
        "fromDate": str(from_date),
        "toDate": str(to_date),

        # Note: you can look up the bankAccountIDs by using the xero.accounts endpoint and filtering account number.
        # This was our old account
        # "bankAccountID": u'9bc4450a-ed06-4049-abbc-03e723581d18',

        # This is our incoming donations account
        "bankAccountID": u'7ee22f07-ffce-4369-a9b3-dc3ce4fa7609',
    }

    bank_transactions = xero.reports.get('BankStatement', params=passed_params)[0]
    desired_headers = [u'Date', u'Reference', u'Amount', u'Our Reference', u'Unique Id']
    xero_headers = [cell[u'Value'] for cell in bank_transactions['Rows'][0]['Cells']]

    # We also write the transactions to a csv file to get a bit of visibility into
    # what's going on for debugging purpose (and because we already wrote the csv export).
    # We add them to the database at the same time.

    FIELD_MAP = [
        # (django_field_name, xero_API_field_name)
        ('date', 'Date'),
        ('bank_statement_text', 'Reference'),
        ('amount', 'Amount'),
        ('reference', 'Our Reference'),
        ('unique_id', 'Unique Id'),
    ]

    with open(os.path.join(base_dir,'eaa_transactions.csv'), 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(desired_headers)

        rows_seen = defaultdict(int)
        for row in bank_transactions['Rows'][1]['Rows']:
            data = dict(zip(xero_headers, [cell[u'Value'] for cell in row[u'Cells']]))

            # Omit "Opening Balance" and "Closing Balance"
            if data[u'Description'] in [u'Opening Balance', u'Closing Balance']:
                continue

            # TODO maybe: change codes to make matching more reliable.
            match = re.search(r'(^|\s)[0-9a-fA-F]{12}($|\s)', data[u'Reference'])
            data[u'Our Reference'] = match.group(0).strip().upper() if match else ''

            # Create a unique id to simplify import. Note that it's more robush to not include the balance in the hash
            # since then if there's a error, e.g., a missing transactions, which does happen in xero from time to time,
            # then fixing it will not cause all later unique id's to change.
            unique_id = hashlib.md5("x".join([data[u'Reference'], str(data[u'Date']), data[u'Amount']])).hexdigest()

            # We generate unique ids for two identical transactions on the same day as follows.
            rows_seen[unique_id] += 1
            if rows_seen[unique_id] > 1:
                unique_id = hashlib.md5(unique_id + str(rows_seen[unique_id])).hexdigest()
            data[u'Unique Id'] = unique_id

            csv_writer.writerow([data[header] for header in desired_headers])

            # Import transactions into database
            kwargs = {}
            for django_field_name, xero_field_name in FIELD_MAP:
                kwargs[django_field_name] = data[xero_field_name]

            BankTransaction.objects.get_or_create(**kwargs)

