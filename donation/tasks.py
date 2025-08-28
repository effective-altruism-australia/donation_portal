import time

from django.conf import settings
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError
from raven.contrib.django.raven_compat.models import client

from donation.models.donation import Donation
from donation.models.pledge import Pledge
from donation_portal.eaacelery import app
from .eaaxero import (
    import_bank_transactions,
    import_trial_balance as import_trial_balance_non_delayed,
)
from .emails import send_bank_transfer_instructions, send_partner_charity_reports
from donation.views.export import write_spreadsheet


@app.task()
def send_bank_transfer_instructions_task(pledge_id):
    send_bank_transfer_instructions(Pledge.objects.get(id=pledge_id))


@app.task()
def process_bank_transactions():
    print("Processing bank transactions...")
    import_bank_transactions(tenant="eaa")
    import_bank_transactions(tenant="eaae")


@app.task()
def import_trial_balance():
    import_trial_balance_non_delayed("eaa")
    import_trial_balance_non_delayed("eaae")


@app.task()
def send_partner_charity_reports_task():
    send_partner_charity_reports(test=False)


@app.task()
def add_pledge_contact_to_mailchimp(pledge_id):
    time.sleep(3)
    mailchimp = MailChimp(
        mc_api=getattr(settings, "MAILCHIMP_API_KEY"), mc_user="eaaustralia"
    )
    pledge = Pledge.objects.get(id=pledge_id)
    assert pledge.subscribe_to_updates
    try:
        mailchimp.lists.members.create(
            "591335048e",
            {
                "email_address": pledge.email,
                "status": "subscribed",
                "source": "Donation form",
                "merge_fields": {
                    "FNAME": pledge.first_name,
                    "LNAME": pledge.last_name,
                },
            },
        )
    except MailChimpError as e:
        if e[0]["title"] not in ("Invalid Resource", "Member Exists"):
            client.captureException()


@app.task()
def add_pledge_contact_to_ea_newsletter(pledge_id):
    mailchimp = MailChimp(mc_api=getattr(settings, "EA_NEWSLETTER_MAILCHIMP_API_KEY"))
    pledge = Pledge.objects.get(id=pledge_id)
    assert pledge.subscribe_to_newsletter
    try:
        mailchimp.lists.members.create(
            "51c1df13ac",
            {
                "email_address": pledge.email,
                "status": "subscribed",
                "source": "Donation form",
                "merge_fields": {
                    "FNAME": pledge.first_name,
                    "LNAME": pledge.last_name,
                },
            },
        )
    except MailChimpError as e:
        if e[0]["title"] not in ("Invalid Resource", "Member Exists"):
            client.captureException()


@app.task()
def export_spreadsheet(location, donation_ids, template):
    donations = Donation.objects.filter(id__in=donation_ids)
    write_spreadsheet(location, {"Donations": donations}, template, cleaned=False)
