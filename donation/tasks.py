from donation_backend.eaacelery import app
from download_bank_transactions import import_bank_transactions
from donation.models import Receipt


def send_all_unsent_receipts():
    for receipt in Receipt.objects.filter(time_sent=None).all():
        receipt.send()


@app.task(bind=True)
def process_bank_transactions(self):
    print("Processing bank transactions...")
    # TODO download receipt spreadsheet
    import_bank_transactions()
    send_all_unsent_receipts()