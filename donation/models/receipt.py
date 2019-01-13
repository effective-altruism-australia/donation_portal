from __future__ import unicode_literals

import os
import random
import string

import arrow
from django.conf import settings
from django.db import models

from .pledge import Pledge
from .transaction import BankTransaction, PinTransaction


class ReceiptManager(models.Manager):
    def create_from_bank_transaction(self, bank_transaction):
        if bank_transaction.date < settings.AUTOMATION_START_DATE:
            return  # no receipt for you
        return self.create(bank_transaction=bank_transaction,
                           pledge=bank_transaction.pledge,
                           email=bank_transaction.pledge.email)

    def create_from_pin_transaction(self, pin_transaction):
        return self.create(pin_transaction=pin_transaction,
                           pledge=pin_transaction.pledge,
                           email=pin_transaction.pledge.email)


class Receipt(models.Model):
    objects = ReceiptManager()
    time_sent = models.DateTimeField(blank=True, null=True)
    # Let's keep receipts around, even if the bank transaction/pledge gets changed/deleted (ideally shouldn't happen).
    bank_transaction = models.ForeignKey(BankTransaction, blank=True, null=True, on_delete=models.SET_NULL)
    pin_transaction = models.ForeignKey(PinTransaction, blank=True, null=True, on_delete=models.SET_NULL)
    pledge = models.ForeignKey(Pledge, blank=True, null=True, on_delete=models.SET_NULL)
    # The email on the pledge might get edited, so let's record the one we used here.
    email = models.EmailField()
    # Note (21 May 17) that the receipt_html field constitutes 90% of the database size
    receipt_html = models.TextField(blank=True, editable=False)
    failed_message = models.TextField(blank=True, editable=False, default='')
    secret = models.CharField(blank=True, max_length=16)  # So the donor can download the receipt from our website.

    @property
    def sent(self):
        return self.time_sent is not None

    @property
    def failed(self):
        return self.failed_message != ''

    @property
    def transaction(self):
        return self.bank_transaction or self.pin_transaction

    @property
    def pdf_receipt_location(self):
        return os.path.join(settings.MEDIA_ROOT, 'receipts', 'EAA_Receipt_{0}.pdf'.format(self.pk))

    @property
    def donation(self):
        if self.bank_transaction:
            return self.bank_transaction.donation
        elif self.pin_transaction:
            return self.pin_transaction.donation
        else:
            raise StandardError('Expected a bank or pin transaction')

    def save(self, *args, **kwargs):
        # Generate a secret for credit card receipts so that people can download them.
        if self.pin_transaction and not self.secret:
            self.secret = ''.join(random.choice(string.letters + string.digits) for _ in range(16))
        super(Receipt, self).save(*args, **kwargs)

    @property
    def status(self):
        if self.sent:
            return "Receipt to {0.email} sent at {1}".format(self,
                                                             arrow.get(self.time_sent).format('YYYY-MM-DD HH:mm:ss'))
        elif self.failed:
            return "Sending failed: {0.failed_message}".format(self)
        else:
            return "Sending failed. No failure message."

    def __unicode__(self):
        if self.bank_transaction:
            transaction_part = ("Receipt for bank donation of ${0.bank_transaction.amount}" +
                                " on {0.bank_transaction.date}").format(self)
        elif self.pin_transaction:
            transaction_part = ("Receipt for credit card donation of ${0.pin_transaction.amount}" +
                                " at {0.pin_transaction.date}").format(self)
        else:
            transaction_part = "Receipt for deleted transaction"
        if self.pledge:
            pledge_part = " by {0.pledge.first_name} {0.pledge.last_name}".format(self)
        else:
            pledge_part = " to {0.email} (pledge deleted)".format(self)
        failed_part = " - Sending failed: {0.failed_message}".format(self) if self.failed else ""
        return transaction_part + pledge_part + failed_part


class EOFYReceipt(models.Model):
    email = models.EmailField()
    year = models.IntegerField()
    time_sent = models.DateTimeField(auto_now_add=True)
    receipt_html_page_1 = models.TextField(blank=True, editable=False)
    receipt_html_page_2 = models.TextField(blank=True, editable=False)
    failed_message = models.TextField(blank=True, editable=False, default='')

    @property
    def sent(self):
        return self.time_sent is not None

    @property
    def failed(self):
        return self.failed_message != ''

    @property
    def pdf_receipt_location(self):
        return os.path.join(settings.MEDIA_ROOT,
                            'eofy_receipts',
                            'EAA_EOFY_Receipt_{0}_{1}.pdf'.format(self.year, self.email)
                            )

    @property
    def status(self):
        if self.sent:
            return "Receipt to {0.email} sent at {1}".format(self,
                                                             arrow.get(self.time_sent).format('YYYY-MM-DD HH:mm:ss'))
        elif self.failed:
            return "Sending failed: {0.failed_message}".format(self)
        else:
            return "Sending failed. No failure message."

    def __unicode__(self):
        details = "{0.year} EOFY Receipt for {0.email}".format(self)
        failed_part = " - Sending failed: {0.failed_message}".format(self) if self.failed else ""
        return details + failed_part
