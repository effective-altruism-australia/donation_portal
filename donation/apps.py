from django.apps import AppConfig
from celery import Celery


class DonationConfig(AppConfig):
    name = "donation"

    def ready(self):
        # Initialize Celery tasks
        app = Celery("donation_portal")
        app.autodiscover_tasks()
        # Load system checks for external dependencies
        try:
            import donation.checks  # noqa: F401
        except ImportError:
            pass
