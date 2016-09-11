from django.conf import settings

from donation.models import Reconciliation, Receipt


def generate_and_send_receipts():
    # Find all reconciled transactions for which we haven't sent receipts
    reconciliations_with_issued_receipts = Receipt.objects.all().values_list('reconciliation_id', flat=True)
    reconciliations_to_do = Reconciliation.objects.filter(bank_transaction__date__gte=settings.AUTOMATION_START_DATE).exclude(id__in=reconciliations_with_issued_receipts).select_related('pledge', 'bank_transaction')
    for reconciliation in reconciliations_to_do[:1]:
        Receipt.objects.create_and_send(reconciliation)
