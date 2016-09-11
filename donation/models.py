import datetime
import pdfkit

from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings



PAYMENT_CHOICES = [
    (1, "Bank"),
    (2, "Cheque")
]

DONATION_FREQUENCIES = [
    (1, "Weekly"),
    (2, "Fortnightly"),
    (3, "Monthly")
]

class Pledge(models.Model):
    completed_time = models.DateTimeField()
    ip = models.GenericIPAddressField()
    reference = models.TextField()
    recipient_org = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.EmailField()
    subscribe_to_updates = models.BooleanField(default=False)
    # TODO use backing field
    # payment_method = models.IntegerField(choices=PAYMENT_CHOICES)
    payment_method_text = models.TextField(blank=True)
    recurring = models.BooleanField()
    # TODO use backing field
    # recurring_frequency = models.IntegerField(choices=DONATION_FREQUENCIES)
    recurring_frequency_text = models.TextField(blank=True)
    publish_donation = models.BooleanField(default=False)
    how_did_you_hear_about_us = models.TextField(blank=True)
    share_with_givewell = models.BooleanField(default=False)
    share_with_gwwc = models.BooleanField(default=False)
    share_with_tlycs = models.BooleanField(default=False)

    # Historical fields from imported data
    drupal_uid = models.IntegerField(default=0)
    drupal_username = models.TextField(blank=True)
    drupal_preferred_donation_method = models.TextField(blank=True)

    def __unicode__(self):
        return "Pledge of {0.amount} to {0.recipient_org} by {0.first_name} {0.last_name}, made on {1}".format(self, self.completed_time.date())


# It's possible that we get the reference wrong when a BankTransaction is imported, for example if the donor
# made a typo. The way we correct this is for one of our staff to edit the reference in the admin so that it
# is correct. Therefore, we pay attention here to whether the reference changes and if it does, we delete the
# old Reconciliation object and create a new one.
class BankTransaction(models.Model):
    date = models.DateField()
    bank_statement_text = models.TextField(blank=True,)
    amount = models.DecimalField(decimal_places=2, max_digits=12,)
    reference = models.TextField(blank=True)
    unique_id = models.TextField(unique=True, editable=False)
    its_not_a_donation = models.BooleanField(default=False)

    def __unicode__(self):
        return ("UNRECONCILED -- " if not self.reconciled else "") + \
            "{0.date} -- {0.amount} -- {0.bank_statement_text}".format(self)

    @property
    def reconciled(self):
        return hasattr(self, 'reconciliation') or self.its_not_a_donation

    @property
    def pledge(self):
        return self.reconciliation.pledge if hasattr(self, 'reconciliation') else None

    # Cache value of reference field on load
    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(BankTransaction, cls).from_db(db, field_names, values)
        instance._loaded_reference = values[field_names.index('reference')]
        return instance

    def save(self, *args, **kwargs):
        if not self._state.adding and (self.reference != self._loaded_reference):
            # Reference changed. Delete any existing reconciliation
            if hasattr(self, 'reconciliation'):
                self.reconciliation.delete()
                self.reconciliation.refresh_from_db()
        super(BankTransaction, self).save(*args, **kwargs)
        self.reconcile_if_necessary()

    def reconcile_if_necessary(self):
        if not hasattr(self, 'reconciliation') and self.reference:
            # Try to find a pledge
            pledges = Pledge.objects.filter(reference=self.reference)
            if len(pledges) > 1:
                raise Exception("Multiple pledges match. This shouldn't happen.")
            elif len(pledges) == 1:
                Reconciliation.objects.create(bank_transaction=self, pledge=pledges[0])


class Reconciliation(models.Model):
    bank_transaction = models.OneToOneField(BankTransaction)
    pledge = models.ForeignKey(Pledge)
    time_reconciled = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return "Donation of {1.amount} by {0.first_name} {0.last_name} on {1.date}".format(
            self.pledge, self.bank_transaction)


class ReceiptManager(models.Manager):
    def create_and_send(self, reconciliation, email=None):
        email = email or reconciliation.pledge.email
        receipt = self.create(reconciliation=reconciliation, email=email)
        receipt.send()
        return receipt


class Receipt(models.Model):
    objects = ReceiptManager
    time_sent = models.DateTimeField(blank=True, null=True)
    # Let's keep receipts around, even if the reconciliation gets changed/deleted.
    reconciliation = models.ForeignKey(Reconciliation, blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    receipt_html = models.TextField(blank=True)

    @property
    def sent(self):
        return self.time_sent is not None

    def send(self):
        self.receipt_html = render_to_string('receipt.html', {'unique_reference': self.pk,
                                                              'pledge': self.reconciliation.pledge,
                                                              'bank_transaction': self.reconciliation.bank_transaction,
                                                              })
        pdf_receipt_location = '/tmp/EAA_Receipt_{0}.pdf'.format(self.pk)
        pdfkit.from_string(self.receipt_html, pdf_receipt_location)

        message = EmailMessage(
            subject='Receipt for donation to Effective Altruism Australia',
            body="""Dear {0.first_name} {0.last_name},

Thank you so much for your donation to Effective Altruism Australia, designated for {0.recipient_org}.

Please find attached your receipt.

Kind regards,

Szun Tay
Effective Altruism Australia
""".format(self.reconciliation.pledge),
            to=["ben.toner@eaa.org.au"],  # TODO
            from_email=settings.POSTMARK_SENDER,
        )
        message.attach_file(pdf_receipt_location, mimetype='application/pdf')
        get_connection().send_messages([message])

        self.time_sent = datetime.datetime.now()
        self.save()
