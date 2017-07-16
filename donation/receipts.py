import arrow
import datetime
import itertools
import os
import pdfkit
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import tempfile

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils import timezone
from django.db.models.functions import Lower

from raven.contrib.django.raven_compat.models import client

from models import Donation, EOFYReceipt


def send_receipt(receipt):
    if receipt.sent:
        raise Exception("Receipt already sent.")
    try:
        # Store receipts in database, for auditing purposes
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


def generate_data_for_eofy_receipts(year):
    # Some donors aren't consistent with the capitalisation of their email address
    donations = (Donation.objects
                 .select_related('pledge')
                 .filter(date__gte=datetime.date(year - 1, 7, 1), date__lt=datetime.date(year, 7, 1))
                 .annotate(email_lower=Lower('pledge__email'))
                 .order_by('email_lower', 'datetime')
                 )
    return [list(donations) for _, donations in itertools.groupby(donations, lambda d: d.email_lower)]


def send_eofy_receipts(test=True):
    year = timezone.now().year
    for donations_from_email in generate_data_for_eofy_receipts(year):
        pledge = donations_from_email[-1].pledge
        email = pledge.email
        context = {'email': email,
                   'name': u"{0.first_name} {0.last_name}".format(pledge),
                   'two_digit_year': year - 2000,
                   'total_amount': sum((donation.amount for donation in donations_from_email)),
                   'donations': donations_from_email,
                   }

        # Enforce not sending multiple receipts by default
        if not test and EOFYReceipt.objects.filter(year=year, email=email, time_sent__isnull=False).exists():
            continue

        eofy_receipt = EOFYReceipt(year=year,
                                   email=email)

        try:
            # Note: wkhtmltopdf can combine multiple html pages into one pdf, but not the version on
            # ubuntu 16.04. Easiest to combine multiple pages using a separate library.

            tempdir = tempfile.mkdtemp()
            merger = PdfFileMerger()

            for page in [1, 2]:
                page_name = 'receipt_html_page_{0}'.format(page)
                html = render_to_string('receipts/eofy_receipt_page_{0}.html'.format(page), context)
                # Store receipts in database, for auditing purposes
                setattr(eofy_receipt, page_name, html)
                file_name = os.path.join(tempdir, page_name + '.pdf')
                pdfkit.from_string(html, file_name)
                merger.append(PdfFileReader(file_name, "rb"))

            merger.write(eofy_receipt.pdf_receipt_location)

            body = render_to_string('receipts/eofy_receipt_message.txt',
                                    {'first_name': pledge.first_name,
                                     'two_digit_year': year - 2000,
                                     })

            message = EmailMessage(
                subject='EOFY Receipt from Effective Altruism Australia',
                body=body,
                to=[email],
                bcc=["info+receipts@eaa.org.au"],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_file(eofy_receipt.pdf_receipt_location, mimetype='application/pdf')
            if not test or email == "@".join(["shop", "bentoner.com"]):
                get_connection().send_messages([message])
                eofy_receipt.time_sent = timezone.now()

        except Exception as e:
            print e
            client.captureException()
            eofy_receipt.failed_message = e.message if e.message else "Sending failed"
        finally:
            shutil.rmtree(tempdir)
        if not test:
            eofy_receipt.save()

