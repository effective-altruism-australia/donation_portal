from django.apps import AppConfig


class DonationConfig(AppConfig):
    name = 'donation'

    def ready(self):
        # Make celery disover these tasks
        from .emails import *
        from .tasks import *
