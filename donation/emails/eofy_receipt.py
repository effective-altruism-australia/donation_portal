import datetime
import itertools

from weasyprint import HTML
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client

from donation.models import Donation, EOFYReceipt


def generate_data_for_eofy_receipts(year, is_eaae):
    # Some donors aren't consistent with the capitalisation of their email address
    donations = (
        Donation.objects.select_related("pledge")
        .filter(
            pledge__is_eaae=is_eaae,
            date__gte=datetime.date(year - 1, 7, 1),
            date__lt=datetime.date(year, 7, 1),
        )
        .annotate(email_lower=Lower("pledge__email"))
        .order_by("email_lower", "datetime")
    )
    return [
        list(donations)
        for _, donations in itertools.groupby(donations, lambda d: d.email_lower)
    ]


def send_eofy_receipts(test=True, year=None, is_eaae=False):
    year = year or timezone.now().year
    for donations_from_email in generate_data_for_eofy_receipts(year, is_eaae):
        pledge = donations_from_email[-1].pledge
        email = pledge.email
        context = {
            "email": email,
            "name": "{0.first_name} {0.last_name}".format(pledge),
            "two_digit_year": year - 2000,
            "total_amount": sum((donation.amount for donation in donations_from_email)),
            "donations": donations_from_email,
            "is_eaae": is_eaae,
            "abn": "57 659 447 417" if is_eaae else "87 608 863 467",
            "base_url": settings.BASE_URL,
        }

        # Enforce not sending multiple receipts by default
        if (
            not test
            and EOFYReceipt.objects.filter(
                year=year, email=email, is_eaae=is_eaae, failed_message=""
            ).exists()
        ):
            continue

        eofy_receipt = EOFYReceipt(year=year, email=email, is_eaae=is_eaae)

        try:
            # Generate both pages as HTML
            page_1_html = render_to_string("receipts/eofy_receipt_page_1.html", context)
            page_2_html = render_to_string("receipts/eofy_receipt_page_2.html", context)

            # Store receipts in database, for auditing purposes
            eofy_receipt.receipt_html_page_1 = page_1_html
            eofy_receipt.receipt_html_page_2 = page_2_html

            # Combine both pages into a single HTML document
            combined_html = (
                page_1_html
                + '<div style="page-break-before: always;"></div>'
                + page_2_html
            )

            # Generate PDF using WeasyPrint
            HTML(string=combined_html).write_pdf(eofy_receipt.pdf_receipt_location)

            context = {
                "first_name": pledge.first_name,
                "two_digit_year": year - 2000,
                "is_eaae": is_eaae,
                "abn": "57 659 447 417" if is_eaae else "87 608 863 467",
                "base_url": settings.BASE_URL,
            }
            body_html = render_to_string("receipts/eofy_receipt_message.html", context)
            body_plain_txt = render_to_string(
                "receipts/eofy_receipt_message.txt", context
            )

            if is_eaae:
                subject = "EOFY Receipt from Effective Altruism Australia Environment"
            else:
                subject = "EOFY Receipt from Effective Altruism Australia"
            message = EmailMultiAlternatives(
                subject=subject,
                body=body_plain_txt,
                to=[email],
                bcc=["info+receipts@eaa.org.au"],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_alternative(body_html, "text/html")
            message.attach_file(
                eofy_receipt.pdf_receipt_location, mimetype="application/pdf"
            )
            if not test or email == settings.TESTING_EMAIL:
                get_connection().send_messages([message])
                eofy_receipt.time_sent = timezone.now()

        except Exception as e:
            client.captureException()
            eofy_receipt.failed_message = str(e) if str(e) else "Sending failed"
        if not test:
            eofy_receipt.save()
