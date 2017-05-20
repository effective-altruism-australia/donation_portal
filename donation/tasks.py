from donation_portal.eaacelery import app

from .eaaxero import import_bank_transactions, import_trial_balance
import reporting

@app.task()
def process_bank_transactions():
    print("Processing bank transactions...")
    import_bank_transactions()
    # Everything else with receipts happens automatically. See donation.models.BankTransaction.save()
    import_trial_balance()


@app.task()
def send_partner_charity_reports():
    reporting.send_partner_charity_reports(test=False)
