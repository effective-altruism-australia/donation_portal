import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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


class BankTransaction(models.Model):
    date = models.DateField()
    bank_statement_text = models.TextField(blank=True,)
    amount = models.DecimalField(decimal_places=2, max_digits=12,)
    reference = models.TextField(blank=True)
    unique_id = models.TextField(unique=True, editable=False)
    its_a_transfer_not_a_donation = models.BooleanField(default=False)

    def __unicode__(self):
        return ("UNRECONCILED -- " if self.needs_to_be_reconciled else "") + \
            "{0.date} -- {0.amount} -- {0.bank_statement_text}".format(self)

    @property
    def needs_to_be_reconciled(self):
        return not (hasattr(self, 'reconciliation') or self.its_a_transfer_not_a_donation)



class Reconciliation(models.Model):
    bank_transaction = models.OneToOneField(BankTransaction)
    pledge = models.ForeignKey(Pledge)
    automatically_reconciled = models.BooleanField(default=False)
    user_who_manually_reconciled = models.ForeignKey(User, blank=True, null=True, editable=False)
    time_reconciled = models.DateTimeField(auto_now_add=True, editable=False)

#    @property
#    def receipt_sent(self):
#        return len(self.objects.receipts.empty


class Receipt(models.Model):
    time_sent = models.DateTimeField()
    transaction = models.ForeignKey(Reconciliation)
    email = models.EmailField()