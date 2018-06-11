from django.apps import AppConfig


class DonationConfig(AppConfig):
    name = 'donation'

    def ready(self):
        from .receipts import send_receipt
