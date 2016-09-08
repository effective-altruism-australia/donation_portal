import pdfkit

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from donation.models import Reconciliation, Receipt


def send_receipt(reconciliation, pdf_receipt_location):
    message = EmailMessage(
        subject='Receipt for donation to Effective Altruism Australia',
        body="""Dear {0.first_name} {0.last_name},

Thank you so much for your donation to {0.recipient_org} via Effective Altruism Australia.

Please find attached your receipt.

Kind regards,

Szun
""".format(reconciliation.pledge),
        to=["ben.toner@eaa.org.au"],
        from_email=settings.POSTMARK_SENDER,
    )
    message.attach_file(pdf_receipt_location, mimetype='application/pdf')
    get_connection().send_messages([message])


def generate_and_send_receipts():
    # Find all reconciled transactions for which we haven't sent receipts
    reconciliations_with_issued_receipts = Receipt.objects.all().values_list('reconciliation_id', flat=True)
    reconciliations_to_do = Reconciliation.objects.filter(bank_transaction__date__gte=settings.AUTOMATION_START_DATE).exclude(id__in=reconciliations_with_issued_receipts).select_related('pledge', 'bank_transaction')
    for reconciliation in reconciliations_to_do[:1]:

        unique_reference = 1000  # TODO
        receipt = render_to_string('receipt.html', {'unique_reference': unique_reference,
                                                    'pledge': reconciliation.pledge,
                                                    'bank_transaction': reconciliation.bank_transaction,})
        pdf_receipt_location = '/tmp/EAA_Receipt_{0}.pdf'.format(unique_reference)
        pdfkit.from_string(receipt, pdf_receipt_location)

        send_receipt(reconciliation, pdf_receipt_location)

        Receipt.objects.create(reconciliation=reconciliation, email=reconciliation.pledge.email, receipt_html=receipt)

