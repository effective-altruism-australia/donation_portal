from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
import sentry_sdk

from donation.models import BankTransferInstruction


def send_bank_transfer_instructions(pledge):
    bank_transfer_instruction, _ = BankTransferInstruction.objects.update_or_create(
        pledge=pledge, defaults={"email": pledge.email}
    )
    try:
        assert not bank_transfer_instruction.sent

        context = {"pledge": pledge, "is_eaae": pledge.is_eaae}
        body = render_to_string("bank_transfer_instructions.txt", context)
        body_html = render_to_string("bank_transfer_instructions.html", context)

        message = EmailMultiAlternatives(
            subject="Instructions to complete your donation",
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
        message.send()

        bank_transfer_instruction.time_sent = timezone.now()

    except Exception as e:
        bank_transfer_instruction.failed_message = e.message
        sentry_sdk.capture_exception()

    bank_transfer_instruction.save()
