import os
import pickle

from django.conf import settings
from django.test import TestCase
from mock import MagicMock
from xero import Xero
from xero.auth import PrivateCredentials

from donation.eaaxero import import_bank_transactions, import_trial_balance


class XeroTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        credentials = PrivateCredentials(settings.XERO_CONSUMER_KEY, settings.XERO_RSA_KEY)
        cls.xero = Xero(credentials)

    def test_import_bank_transactions(self):
        with open(os.path.join(settings.BASE_DIR, 'donation/tests/data/bank_transactions.txt'), "rb") as myFile:
            bank_transactions = pickle.load(myFile)

        self.xero.reports.get = MagicMock(return_value=bank_transactions)
        import_bank_transactions()

    def test_import_trial_balance(self):
        with open(os.path.join(settings.BASE_DIR, 'donation/tests/data/trial_balance.txt'), "rb") as myFile:
            trial_balance = pickle.load(myFile)
        self.xero.reports.get = MagicMock(return_value=trial_balance)
        import_trial_balance()
