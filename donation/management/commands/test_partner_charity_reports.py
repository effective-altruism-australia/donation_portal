from django.core.management.base import BaseCommand

from donation.reporting import send_partner_charity_reports


class Command(BaseCommand):
    help = 'Test send partner charity reports'

    def handle(self, *args, **options):
        send_partner_charity_reports(test=True)
