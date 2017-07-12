import arrow
import pdfkit

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
from django.conf import settings
from django.utils import timezone

from raven.contrib.django.raven_compat.models import client


# TODO better tracking of these messages
def send_bank_transfer_instructions(pledge):
    try:
        context = {'pledge': pledge, 'partner_charity': pledge.recipient_org.name}
        body = render_to_string('bank_transfer_instructions.txt', context)
        body_html = render_to_string('bank_transfer_instructions.html', context)

        message = EmailMultiAlternatives(
            subject='Instructions to complete your donation',
            body=body,
            to=[pledge.email],
            # cc=[self.pledge.recipient_org.email],
            # There is a filter in info@eaa.org.au
            #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
            # that automatically archives messages sent to info+receipt and adds the label 'receipts'
            # bcc=["info+receipt@eaa.org.au", ],
            cc=["info@eaa.org.au"],
            from_email=settings.POSTMARK_SENDER,
        )
        message.attach_alternative(body_html, "text/html")
        get_connection().send_messages([message])

    except Exception as e:
        client.captureException()
        pledge.failed_message = e.message if e.message else "Sending failed"


def send_receipt(receipt):
    if receipt.sent:
        raise Exception("Receipt already sent.")
    try:
        receipt.receipt_html = render_to_string('receipts/receipt.html',
                                                {'unique_reference': receipt.pk,
                                                 'pledge': receipt.pledge,
                                                 'transaction': receipt.transaction,
                                                 })
        pdfkit.from_string(receipt.receipt_html, receipt.pdf_receipt_location)

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
                                 'eofy_receipt_date': eofy_receipt_date,
                                 })
        message = EmailMessage(
            subject='Receipt for your donation to Effective Altruism Australia',
            body=body,
            to=[receipt.pledge.email],
            cc=[receipt.pledge.recipient_org.email],
            # There is a filter in info@eaa.org.au
            #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
            # that automatically archives messages sent to info+receipt and adds the label 'receipts'
            # bcc=["info+receipt@eaa.org.au", ],
            bcc=["info+receipts@eaa.org.au"],
            from_email=settings.POSTMARK_SENDER,
        )
        message.attach_file(receipt.pdf_receipt_location, mimetype='application/pdf')
        get_connection().send_messages([message])

        receipt.time_sent = timezone.now()
    except Exception as e:
        client.captureException()
        receipt.failed_message = e.message if e.message else "Sending failed"
    receipt.save()
