from donation_backend.eaacelery import app
from download_bank_transactions import import_bank_transactions
from reconcile import reconcile
from receipt import generate_and_send_receipts


@app.task(bind=True)
def process_bank_transactions(self):
    print("Processing bank transactions...")
    # TODO download receipt spreadsheet
    import_bank_transactions()
    reconcile()
    generate_and_send_receipts()

