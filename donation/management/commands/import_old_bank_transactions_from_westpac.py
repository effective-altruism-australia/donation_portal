from datetime import date
from django.core.management.base import BaseCommand

from donation.eaaxero import import_bank_transactions_from_account


class Command(BaseCommand):
    help = "Manually import from xero donations in old Westpac account"

    def handle(self, *args, **options):
        import_bank_transactions_from_account(
            "9bc4450a-ed06-4049-abbc-03e723581d18",
            date(2015, 12, 1),
            date(2016, 10, 1),
            manual=True,
        )
        self.stdout.write("Successfully imported data from xero")
