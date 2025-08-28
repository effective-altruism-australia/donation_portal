import datetime
import os
import pickle

from django.conf import settings
from xero import Xero
from xero.auth import PrivateCredentials

credentials = PrivateCredentials(settings.XERO_CONSUMER_KEY, settings.XERO_RSA_KEY)
xero = Xero(credentials)


def generate_xero_bank_data_for_tests():
    passed_params = {
        "fromDate": str(datetime.date(2018, 7, 29)),
        "toDate": str(datetime.date(2018, 8, 1)),
        "bankAccountID": settings.XERO_INCOMING_ACCOUNT_ID_DICT["eaa"],
    }
    bank_transactions = xero.reports.get("BankStatement", params=passed_params)
    bank_transactions[0]["Rows"][1]["Rows"] = bank_transactions[0]["Rows"][1]["Rows"][
        0:5
    ]  # Keep first 5

    for row in bank_transactions[0]["Rows"][1]["Rows"][1:]:
        row["Cells"][2]["Value"] = "Description goes here"

    with open(
        os.path.join(settings.BASE_DIR, "donation/tests/data/bank_transactions.txt"),
        "wb",
    ) as myFile:
        pickle.dump(bank_transactions, myFile)


def generate_xero_trial_balance_data_for_test():
    balance_date = datetime.date(2018, 1, 31)
    trial_balance = xero.reports.get("TrialBalance", params={"Date": balance_date})
    del trial_balance[0]["Rows"][2:]
    del trial_balance[0]["Rows"][1]["Rows"][1:]
    trial_balance[0]["Rows"][1]["Rows"][0]["Cells"][0]["Value"] = "Test"

    with open(
        os.path.join(settings.BASE_DIR, "donation/tests/data/trial_balance.txt"), "wb"
    ) as myFile:
        pickle.dump(trial_balance, myFile)
