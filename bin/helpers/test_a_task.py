import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donation_portal.settings')
django.setup()

# Now import your task
from donation.tasks import send_partner_charity_reports_task
from donation_portal.eaacelery import app

# Run the task
send_partner_charity_reports_task()