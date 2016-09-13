from donation_backend.eaacelery import app
from download_bank_transactions import import_bank_transactions


@app.task(bind=True)
def process_bank_transactions(self):
    print("Processing bank transactions...")
    # TODO download receipt spreadsheet
    import_bank_transactions()
