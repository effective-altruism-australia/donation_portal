from django.apps import AppConfig


class DonationConfig(AppConfig):
    name = 'donation'

    def ready(self):
        from .emails import *  # Make celery disover these tasks
