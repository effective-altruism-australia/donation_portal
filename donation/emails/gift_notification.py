from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from raven.contrib.django.raven_compat.models import client

from donation.models import Donation
from donation_portal.eaacelery import app


@app.task()
def send_gift_notification(donation_id):
    try:
        donation = Donation.objects.get(id=donation_id)
        pledge = donation.pledge
        assert pledge.is_gift, 'Expected the pledge to be marked as a gift'
        assert not pledge.gift_message_sent, 'Gift message has already been sent'
        context = {
            'pledge': pledge,
            'donation': donation,
            'personal_message': mark_safe(pledge.gift_personal_message)
        }
        body_html = render_to_string('gift_message.html', context)
        body_plain_txt = render_to_string('gift_message.txt', context)

        message = EmailMultiAlternatives(
            subject='%s has made a donation on your behalf' % pledge.first_name,
            body=body_plain_txt,
            to=[pledge.gift_recipient_email],
            cc=[settings.EAA_INFO_EMAIL, pledge.email],
            from_email=settings.POSTMARK_SENDER,

        )
        message.attach_alternative(body_html, "text/html")
        message.send()

        pledge.gift_message_sent = True
        pledge.save()
    except Exception as e:
        print e.message
        client.captureException()
