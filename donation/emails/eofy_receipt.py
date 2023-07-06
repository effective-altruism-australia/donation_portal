import datetime
import itertools
import os
import shutil
import tempfile

import pdfkit
from PyPDF2 import PdfFileReader, PdfFileMerger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client
from tqdm import tqdm
from donation.models import Donation, EOFYReceipt


def generate_data_for_eofy_receipts(year, is_eaae):
    # Some donors aren't consistent with the capitalisation of their email address
    donations = (Donation.objects
                 .select_related('pledge')
                 .filter(pledge__is_eaae=is_eaae,
                         date__gte=datetime.date(year - 1, 7, 1), date__lt=datetime.date(year, 7, 1))
                 .annotate(email_lower=Lower('pledge__email'))
                 .order_by('email_lower', 'datetime')
                 )
    return [list(donations) for _, donations in itertools.groupby(donations, lambda d: d.email_lower)]


def send_eofy_receipts(test=True, year=None, is_eaae=False):
    year = year or timezone.now().year
    for donations_from_email in tqdm(generate_data_for_eofy_receipts(year, is_eaae)):
        pledge = donations_from_email[-1].pledge
        email = pledge.email
        context = {'email': email,
                   'name': u"{0.first_name} {0.last_name}".format(pledge),
                   'two_digit_year': year - 2000,
                   'total_amount': sum((donation.amount for donation in donations_from_email)),
                   'donations': donations_from_email,
                   }

        # Enforce not sending multiple receipts by default
        if not test and EOFYReceipt.objects.filter(year=year, email=email, time_sent__isnull=False,
                                                   is_eaae=is_eaae).exists():
            continue

        eofy_receipt = EOFYReceipt(year=year,
                                   email=email,
                                   is_eaae=is_eaae)

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

            context = {'first_name': pledge.first_name,
                       'two_digit_year': year - 2000,
                       }
            body_html = render_to_string('receipts/eofy_receipt_message.html', context)
            body_plain_txt = render_to_string('receipts/eofy_receipt_message.txt', context)

            message = EmailMultiAlternatives(
                subject='EOFY Receipt from Effective Altruism Australia',
                body=body_plain_txt,
                to=[email],
                bcc=["info+receipts@eaa.org.au"],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_alternative(body_html, "text/html")
            message.attach_file(eofy_receipt.pdf_receipt_location, mimetype='application/pdf')
            if not test or email == settings.TESTING_EMAIL:
                get_connection().send_messages([message])
                eofy_receipt.time_sent = timezone.now()

        except Exception as e:
            client.captureException()
            eofy_receipt.failed_message = e.message if e.message else "Sending failed"
        finally:
            shutil.rmtree(tempdir)
        if not test:
            eofy_receipt.save()
