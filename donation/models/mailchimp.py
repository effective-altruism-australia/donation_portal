from django.conf import settings
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError
from raven.contrib.django.raven_compat.models import client

from donation.models import Pledge
from donation_portal.eaacelery import app

mailchimp = MailChimp(mc_api=getattr(settings, 'MAILCHIMP_API_KEY'), mc_user='eaaustralia')


@app.task()
def add_pledge_contact_to_mailchimp(pledge_id):
    pledge = Pledge.objects.get(id=pledge_id)
    assert pledge.subscribe_to_updates
    try:
        mailchimp.lists.members.create('591335048e', {
            'email_address': pledge.email,
            'status': 'subscribed',
            'source': 'Donation form',
            'merge_fields': {
                'FNAME': pledge.first_name,
                'LNAME': pledge.last_name,
            },
        })
    except MailChimpError as e:
        if e[0]['title'] not in ('Invalid Resource', 'Member Exists'):
            client.captureException()
