from models import BankTransaction, Pledge, Reconciliation

def reconcile():
    reconciled_bank_transactions = Reconciliation.objects.all().values_list('bank_transaction_id', flat=True)
    bank_transactions_to_be_reconciled = BankTransaction.objects.filter(its_a_transfer_not_a_donation=False).exclude(id__in=reconciled_bank_transactions)
    for bank_transaction in bank_transactions_to_be_reconciled:
        if bank_transaction.reference:
            # Try to find a pledge
            pledges = Pledge.objects.filter(reference=bank_transaction.reference)
            if len(pledges) > 1:
                raise Exception("Multiple pledges match. This shouldn't happen.")
            elif len(pledges) == 1:
                Reconciliation.objects.create(bank_transaction=bank_transaction, pledge=pledges[0],
                                              automatically_reconciled=True)