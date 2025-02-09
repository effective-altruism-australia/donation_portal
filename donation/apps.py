from django.apps import AppConfig
from celery import Celery


class DonationConfig(AppConfig):
    name = 'donation'

    def ready(self):
        app = Celery('donation_portal')
        app.autodiscover_tasks()