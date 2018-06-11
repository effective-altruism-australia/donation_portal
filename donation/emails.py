from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from raven.contrib.django.raven_compat.models import client


# TODO better tracking of these messages
def send_bank_transfer_instructions(pledge):
    try:
        context = {'pledge': pledge}
        body = render_to_string('bank_transfer_instructions.txt', context)
        body_html = render_to_string('bank_transfer_instructions.html', context)

        message = EmailMultiAlternatives(
            subject='Instructions to complete your donation',
            body=body,
            to=[pledge.email],
            # There is a filter in info@eaa.org.au
            #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
            # that automatically archives messages sent to info+receipt and adds the label 'receipts'
            # bcc=["info+receipt@eaa.org.au", ],
            cc=[settings.EAA_INFO_EMAIL],
            from_email=settings.POSTMARK_SENDER,
        )
        message.attach_alternative(body_html, "text/html")
        get_connection().send_messages([message])

    except Exception as e:
        client.captureException()


def send_gift_notification(pledge):
    try:
        assert pledge.is_gift, 'Expected the pledge to be marked as a gift'
        assert not pledge.gift_message_sent, 'Gift message has already been sent'
        context = {'pledge': pledge}
        body = render_to_string('gift_message.txt', context)

        message = EmailMultiAlternatives(
            subject='%s has made a donation on your behalf' % pledge.first_name,
            body=body,
            to=[pledge.gift_recipient_email],
            cc=[settings.EAA_INFO_EMAIL],
            from_email=settings.POSTMARK_SENDER,
        )
        get_connection().send_messages([message])

        pledge.gift_message_sent = True
        pledge.save()
    except Exception as e:
        client.captureException()
