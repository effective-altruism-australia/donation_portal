from donation_portal.eaacelery import app

from .eaaxero import import_bank_transactions, import_trial_balance
from .drupal_import import reconcile_imported_pledges


@app.task()
def process_bank_transactions():
    print("Processing bank transactions...")
    # TODO download receipt spreadsheet
    import_bank_transactions()
    # Everything else with receipts happens automatically. See donation.models.BankTransaction.save()
    import_trial_balance()


@app.task()
def reconcile_pledges_imported_from_drupal():
    print("Reconciling pledges from drupal...")
    reconcile_imported_pledges()
