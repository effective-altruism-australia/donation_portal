from django.core.management.base import BaseCommand

from donation.emails import send_eofy_receipts


class Command(BaseCommand):
    help = 'Send EOFY receipts'

    def handle(self, *args, **options):
        send_eofy_receipts(test=False)
