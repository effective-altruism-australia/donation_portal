from __future__ import unicode_literals

import pdfkit
import arrow
import re
import os

from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client
from enumfields import EnumField, Enum

from pinpayments.models import PinTransaction as BasePinTransaction


class PartnerCharity(models.Model):
    name = models.TextField(unique=True)
    email = models.EmailField(help_text="Used to cc the charity on receipts")
    xero_account_name = models.TextField(help_text="Exact text of incoming donation account in xero")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Partner charities"


class PaymentMethod(Enum):
    BANK = 1
    CHEQUE = 2
    CREDIT_CARD = 3
    PAYPAL = 4


class RecurringFrequency(Enum):
    WEEKLY = 1
    FORTNIGHTLY = 2
    MONTHLY = 3


# Copy choices from drupal for transition
HOW_DID_YOU_HEAR_CHOICES = ["The Life You Can Save",
                            "News",
                            "Advertising",
                            "GiveWell",
                            "From the charity (SCI, Evidence Action, GiveDirectly)",
                            "Search engine (Google etc.)",
                            "Friend",
                            "Giving What We Can"
                            ]


class Pledge(models.Model):
    completed_time = models.DateTimeField()
    ip = models.GenericIPAddressField(null=True)
    reference = models.TextField()
    recipient_org = models.ForeignKey(PartnerCharity)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    first_name = models.CharField(max_length=1024, blank=True)  # TODO safely decrease length
    last_name = models.CharField(max_length=1024, blank=True)  # TODO safely decrease length
    email = models.EmailField()
    subscribe_to_updates = models.BooleanField(default=False, verbose_name='Send me latest news and updates')
    payment_method = EnumField(PaymentMethod, max_length=1)
    recurring = models.BooleanField(default=False)
    recurring_frequency = EnumField(RecurringFrequency, max_length=1, blank=True, null=True)
    publish_donation = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.TextField(blank=True, null=True,
                                                 choices=zip(HOW_DID_YOU_HEAR_CHOICES, HOW_DID_YOU_HEAR_CHOICES),
                                                 verbose_name='How did you hear about us?')
    share_with_givewell = models.BooleanField(default=False)
    share_with_gwwc = models.BooleanField(default=False)
    share_with_tlycs = models.BooleanField(default=False)

    # Historical fields from imported data
    drupal_uid = models.IntegerField(default=0, editable=False)
    drupal_username = models.TextField(blank=True, editable=False)
    drupal_preferred_donation_method = models.TextField(blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.completed_time:
            self.completed_time = timezone.now()
        super(Pledge, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Pledge of ${0.amount} to {0.recipient_org} by {0.first_name} {0.last_name}, " \
            "made on {1}. Reference {0.reference}".format(self, self.completed_time.date())


# It's possible that we get the reference wrong when a BankTransaction is imported, for example if the donor
# made a typo. The way we correct this is for one of our staff to edit the reference in the admin so that it
# is correct. Therefore, we pay attention here to whether the reference changes and if it does, we delete the
# existing Pledge (if any) and search for a matching one.
class BankTransaction(models.Model):
    date = models.DateField()
    bank_statement_text = models.TextField(blank=True,)
    amount = models.DecimalField(decimal_places=2, max_digits=12,)
    reference = models.TextField(blank=True)
    unique_id = models.TextField(unique=True, editable=False)
    do_not_reconcile = models.BooleanField(default=False)
    pledge = models.ForeignKey(Pledge, blank=True, null=True)
    time_reconciled = models.DateTimeField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return ("UNRECONCILED -- " if not self.reconciled else "") + \
            "{0.date} -- {0.amount} -- {0.bank_statement_text}".format(self)

    @property
    def reconciled(self):
        return self.pledge is not None or self.do_not_reconcile

    # Cache value of reference field on load
    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(BankTransaction, cls).from_db(db, field_names, values)
        instance._loaded_reference = values[field_names.index('reference')]
        return instance

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.find_reference_in_bank_statement_text()
        elif self.reference != self._loaded_reference:
            # Reference changed. Delete any existing pledge
            self.pledge = None
        # Things marked 'do_not_reconcile' should have any existing reconciliation removed
        if self.do_not_reconcile:
            self.pledge = None
            self.reference = ''
        # Save it immediately because there could be an exception trying to reconcile
        super(BankTransaction, self).save(*args, **kwargs)
        matched_with_pledge = self.reconcile()
        if matched_with_pledge:
            kwargs['force_insert'] = False  # can't force_insert twice
            super(BankTransaction, self).save(*args, **kwargs)
            # Generate a receipt object.
            Receipt.objects.create_from_bank_transaction(self)

    def reconcile(self):
        if self.pledge is None and self.reference:
            # Try to find a matching pledge
            pledges = Pledge.objects.filter(reference=self.reference)
            if len(pledges) > 1:
                raise Exception("Multiple pledges match. This shouldn't happen.")
            elif len(pledges) == 1:
                self.pledge = pledges[0]
                return True

    class NotReconciledException(Exception):
        pass

    def resend_receipt(self):
        if not self.pledge:
            raise BankTransaction.NotReconciledException("Can't send receipt, transaction is not reconciled.")
        Receipt.objects.create_from_bank_transaction(self)

    def find_reference_in_bank_statement_text(self):
        # TODO do this by lookup, after switching form from drupal. We won't do that now,
        # since we may import bank statements before pledges.
        match = re.search(r'(^|\s)[0-9a-fA-F]{12}($|\s)', self.bank_statement_text)
        self.reference = match.group(0).strip().upper() if match else ''


class PinTransaction(BasePinTransaction):
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE)


class ReceiptManager(models.Manager):
    def create_from_bank_transaction(self, bank_transaction):
        if bank_transaction.date < settings.AUTOMATION_START_DATE:
            return  # no receipt for you
        return self.create(bank_transaction=bank_transaction,
                           pledge=bank_transaction.pledge,
                           email=bank_transaction.pledge.email)

    def create(self, *args, **kwargs):
        receipt = super(ReceiptManager, self).create(*args, **kwargs)
        receipt.send()
        return receipt


class Receipt(models.Model):
    objects = ReceiptManager()
    time_sent = models.DateTimeField(blank=True, null=True)
    # Let's keep receipts around, even if the bank transaction/pledge gets changed/deleted (ideally shouldn't happen).
    bank_transaction = models.ForeignKey(BankTransaction, blank=True, null=True, on_delete=models.SET_NULL)
    pledge = models.ForeignKey(Pledge, blank=True, null=True, on_delete=models.SET_NULL)
    # The email on the pledge might get edited, so let's record the one we used here.
    email = models.EmailField()
    receipt_html = models.TextField(blank=True, editable=False)
    failed_message = models.TextField(blank=True, editable=False, default='')

    @property
    def sent(self):
        return self.time_sent is not None

    @property
    def failed(self):
        return self.failed_message != ''

    def send(self):
        if self.sent:
            raise Exception("Receipt already sent.")
        try:
            self.receipt_html = render_to_string('receipt.html', {'unique_reference': self.pk,
                                                                  'pledge': self.pledge,
                                                                  'bank_transaction': self.bank_transaction,
                                                                  })
            pdf_receipt_location = os.path.join(settings.MEDIA_ROOT, 'receipts', 'EAA_Receipt_{0}.pdf'.format(self.pk))
            pdfkit.from_string(self.receipt_html, pdf_receipt_location)

            now = arrow.now()
            eofy_receipt_date = now.replace(month=7).replace(day=31).replace(years=+1 if now.month > 6 else 0).date()

            body = render_to_string('receipt_message.txt', {'pledge': self.pledge,
                                                            'bank_transaction': self.bank_transaction,
                                                            'eofy_receipt_date': eofy_receipt_date,
                                                            })
            message = EmailMessage(
                subject='Receipt for your donation to Effective Altruism Australia',
                body=body,
                to=[self.pledge.email],
                cc=[self.pledge.recipient_org.email],
                # There is a filter in info@eaa.org.au
                #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
                # that automatically archives messages sent to info+receipt and adds the label 'receipts'
                # bcc=["info+receipt@eaa.org.au", ],
                bcc=["info+receipts@eaa.org.au"],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_file(pdf_receipt_location, mimetype='application/pdf')
            get_connection().send_messages([message])

            self.time_sent = timezone.now()
        except Exception as e:
            client.captureException()
            self.failed_message = e.message if e.message else "Sending failed"
        self.save()

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
            bank_transaction_part = ("Receipt for donation of ${0.bank_transaction.amount}" +
                                     " on {0.bank_transaction.date}").format(self)
        else:
            bank_transaction_part = "Receipt for deleted bank transaction"
        if self.pledge:
            pledge_part = " by {0.pledge.first_name} {0.pledge.last_name}".format(self)
        else:
            pledge_part = " to {0.email} (pledge deleted)".format(self)
        failed_part = " - Sending failed: {0.failed_message}".format(self) if self.failed else ""
        return bank_transaction_part + pledge_part + failed_part


class Account(models.Model):
    # xero is the authoritative source of funds raised to date. We use this class to store information about total
    # donations received in any given month.
    date = models.DateField()  # Should be an end of month
    name = models.TextField()

    # This is the total of account transactions in that month.
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    # Let's just store the year to date number too, whatever
    ytd_amount = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        unique_together = ('date', 'name', )


class XeroReconciledDate(models.Model):
    # Up to and including this date, we take total donation information from xero. After this date, we use the
    # BankTransaction objects. The BankTransaction objects will be missing things like workplace giving.
    date = models.DateField()

    def __unicode__(self):
        return str(self.date)


@receiver(post_save, sender=XeroReconciledDate)
def reload_xero_data(sender, instance, **kwargs):
    # Reload up-to-date data from xero after advancing the date
    # Do it on on user's thread not via celery for obviousness.
    # Lazy imports because circular dependencies
    from eaaxero import import_trial_balance
    import_trial_balance()


class TransitionalDonationsFile(models.Model):
    # The download from drupal
    time_uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')


@receiver(post_save, sender=TransitionalDonationsFile)
def import_pledges(sender, instance, **kwargs):
    # Lazy imports because circular dependencies
    from .drupal_import import import_from_drupal
    from .tasks import reconcile_pledges_imported_from_drupal
    import_from_drupal(instance)
    reconcile_pledges_imported_from_drupal.delay()
