from django.core.management.base import BaseCommand

from donation.emails import send_eofy_receipts


class Command(BaseCommand):
    help = 'Test EOFY receipts'

    def handle(self, *args, **options):
        send_eofy_receipts(test=True, is_eaae=False)
        send_eofy_receipts(test=True, is_eaae=True)

