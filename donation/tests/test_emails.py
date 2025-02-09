from django.core import mail
from django.test import TestCase
from django.utils import timezone
from mock import MagicMock
from model_mommy import mommy

from donation.emails import email_receipt, send_bank_transfer_instructions, send_eofy_receipts, \
    send_gift_notification, send_partner_charity_reports
from donation.models import PledgeComponent, BankTransaction, Receipt, Pledge, EOFYReceipt, PartnerCharityReport, \
    PartnerCharity


class EmailTestCase(TestCase):
    def setUp(self):
        partner_charity = mommy.make(PartnerCharity, name='Friendly Partner Name')
        self.pledge = mommy.make(Pledge, email='nathan.sherburn@eaa.org.au')
        mommy.make(PledgeComponent, pledge=self.pledge, partner_charity=partner_charity)
        self.bank_transaction = mommy.make(BankTransaction, amount=self.pledge.amount, pledge=self.pledge)

    def assert_emails_sent(self, num=1):
        self.assertEqual(len(mail.outbox), num)

    def test_bank_transfer_instructions(self):
        send_bank_transfer_instructions(self.pledge)
        self.assertTrue(self.pledge.banktransferinstruction.sent)
        self.assert_emails_sent()

    def test_receipt(self):
        email_receipt.delay = MagicMock(side_effect=email_receipt)  # Don't send task to celery
        receipt = mommy.make(Receipt, bank_transaction=self.bank_transaction, pledge=self.pledge)
        receipt.refresh_from_db()
        self.assertTrue(receipt.sent)
        self.assert_emails_sent()

    def test_eofy_receipts(self):
        current_fy = timezone.now().year
        if timezone.now().month >= 7:
            current_fy += 1

        send_eofy_receipts(test=False, year=current_fy)
        eofy_receipt = EOFYReceipt.objects.get()
        self.assertIsNotNone(eofy_receipt.receipt_html_page_1)
        self.assertIsNotNone(eofy_receipt.receipt_html_page_2)
        self.assertTrue(eofy_receipt.sent)
        self.assert_emails_sent()

    def test_gift_notification(self):
        # Test that the email is not sent if the pledge is not a gift
        send_gift_notification(self.bank_transaction.donation.id)
        self.assertFalse(self.pledge.gift_message_sent)
        # Test that the email is sent if the pledge is a gift
        self.pledge.is_gift = True
        self.pledge.gift_recipient_email = 'test@example.com'
        self.pledge.save()
        send_gift_notification(self.bank_transaction.donation.id)
        self.pledge.refresh_from_db()
        self.assertTrue(self.pledge.gift_message_sent)
        self.assert_emails_sent()

    def test_partner_charity_reports(self):
        send_partner_charity_reports(test=False)
        self.assertIsNotNone(PartnerCharityReport.objects.get(partner=self.pledge.components.first().partner_charity
                                                              ).time_sent)
        self.assertGreater(len(mail.outbox), 0)
