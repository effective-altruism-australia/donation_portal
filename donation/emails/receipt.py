import time

import arrow
import pdfkit
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client

from donation.models import Receipt
from donation_portal.eaacelery import app
from .gift_notification import send_gift_notification


@receiver(post_save, sender=Receipt)
def create_and_send_receipt(sender, instance, created, **kwargs):
    if created:
        receipt = instance
        if receipt.sent:
            raise Exception("Receipt already sent.")
        try:
            if receipt.pledge.is_gift and not receipt.pledge.gift_message_sent:
                send_gift_notification.delay(receipt.pledge.id)
            # Store receipts in database, for auditing purposes
            receipt.receipt_html = render_to_string('receipts/receipt.html',
                                                    {'unique_reference': receipt.pk,
                                                     'pledge': receipt.pledge,
                                                     'transaction': receipt.transaction,
                                                     })
            pdfkit.from_string(receipt.receipt_html, receipt.pdf_receipt_location)
            receipt.save()

            email_receipt.delay(receipt.id)

        except Exception as e:
            client.captureException()
            receipt.failed_message = e.message if e.message else "Sending failed"
            receipt.save()


@app.task()
def email_receipt(receipt_id):
    # HACK: There appears to be a weird race condition where the receipt doesnt get committed quickly enough
    # So we just wait a second.
    time.sleep(1)
    receipt = Receipt.objects.get(id=receipt_id)
    if receipt.sent:
        raise Exception("Receipt already sent.")
    try:
        if receipt.bank_transaction:
            received_date = receipt.bank_transaction.date
        else:
            received_date = arrow.get(receipt.pin_transaction.date).to(settings.TIME_ZONE).date()
        eofy_receipt_date = (arrow.get(received_date)
                             .replace(month=7)
                             .replace(day=31)
                             .shift(years=+1 if received_date.month > 6 else 0)
                             .date())

        body = render_to_string('receipts/receipt_message.txt',
                                {'pledge': receipt.pledge,
                                 'transaction': receipt.transaction,
                                 'date_str': receipt.transaction.date.strftime('%-d %b %Y at %-I:%M%p'),
                                 'eofy_receipt_date': eofy_receipt_date,
                                 })
        message = EmailMessage(
            subject='Receipt for your donation to Effective Altruism Australia',
            body=body,
            to=[receipt.pledge.email],
            # There is a filter in info@eaa.org.au
            #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
            # that automatically archives messages sent to info+receipt and adds the label 'receipts'
            # bcc=["info+receipt@eaa.org.au", ],
            bcc=[settings.EAA_INFO_EMAIL],
            from_email=settings.POSTMARK_SENDER,
        )
        message.attach_file(receipt.pdf_receipt_location, mimetype='application/pdf')
        message.send()
        receipt.time_sent = timezone.now()
    except Exception as e:
        client.captureException()
        receipt.failed_message = e.message if e.message else "Sending failed"
    receipt.save()
