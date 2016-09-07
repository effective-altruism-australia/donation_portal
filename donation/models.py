from django.db import models

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


class BankTransaction(models.Model):
    date = models.DateField(editable=False)
    bank_statement_text = models.TextField(blank=True, editable=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12, editable=False)
    reference = models.TextField(blank=True)
    unique_id = models.TextField(unique=True, editable=False)


class Reconciliation(models.Model):
    bank_transaction = models.ForeignKey(BankTransaction)
    pledge = models.ForeignKey(Pledge)
    automatically_reconciled = models.BooleanField(default=False)

#    @property
#    def receipt_sent(self):
#        return len(self.objects.receipts.empty


class Receipt(models.Model):
    time_sent = models.DateTimeField()
    transaction = models.ForeignKey(Reconciliation)
    email = models.EmailField()