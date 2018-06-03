from __future__ import unicode_literals

import json
import os
import random
import re
import string

import arrow
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from enumfields import Enum, EnumIntegerField
from pinpayments.models import PinTransaction as BasePinTransaction


class PartnerCharity(models.Model):
    slug_id = models.CharField(max_length=30, unique=True, null=True)
    name = models.TextField(unique=True, verbose_name='Name (human readable)')
    email = models.EmailField(help_text="Used to cc the charity on receipts")
    xero_account_name = models.TextField(help_text="Exact text of incoming donation account in xero")
    active = models.BooleanField(default=True)

    order = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Partner charities"

    _cached_database_ids = None

    @classmethod
    def cache_database_ids(cls):
        cls._cached_database_ids = json.dumps({x['name']: x['id'] for x in cls.objects.all().values('name', 'id')})

    @classmethod
    def get_cached_database_ids(cls):
        if not cls._cached_database_ids:
            cls.cache_database_ids()
        return cls._cached_database_ids

    def save(self, *args, **kwargs):
        super(PartnerCharity, self).save(*args, **kwargs)
        PartnerCharity.cache_database_ids()


class PaymentMethod(Enum):
    BANK = 1
    CHEQUE = 2
    CREDIT_CARD = 3
    PAYPAL = 4


class RecurringFrequency(Enum):
    WEEKLY = 1
    FORTNIGHTLY = 2
    MONTHLY = 3


class ReferralSource(models.Model):
    slug_id = models.CharField(max_length=30, unique=True, null=True)
    reason = models.CharField(max_length=256, help_text="Instead of editing this text, you probably want to "
                                                        "disable this ReferralSource and create a new one. If you edit "
                                                        "this, you'll also update the referral sources for donations "
                                                        "already made.",
                              unique=True)
    enabled = models.BooleanField(default=True)
    order = models.BigIntegerField(blank=True, null=True,
                                   help_text='Enter an integer. Reasons will be ordered from smallest to largest.')

    def __str__(self):
        return '{}{}'.format('(DISABLED) ' if not self.enabled else '', self.reason)


class Pledge(models.Model):
    completed_time = models.DateTimeField()
    ip = models.GenericIPAddressField(null=True)
    reference = models.TextField(blank=True)
    # TODO: Remove, this is now captured by PledgeComponent
    recipient_org = models.ForeignKey(PartnerCharity, null=True)
    # TODO: Consider deleting and using the amount_from_components property
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    first_name = models.CharField(max_length=1024, blank=True, verbose_name='name')  # TODO safely decrease length
    last_name = models.CharField(max_length=1024, blank=True)  # TODO safely decrease length
    email = models.EmailField()
    subscribe_to_updates = models.BooleanField(default=False, verbose_name='Send me news and updates')
    payment_method = EnumIntegerField(PaymentMethod)
    recurring = models.BooleanField(default=False)
    recurring_frequency = EnumIntegerField(RecurringFrequency, blank=True, null=True)
    publish_donation = models.BooleanField(default=False)
    how_did_you_hear_about_us_db = models.ForeignKey(ReferralSource, blank=True, null=True, on_delete=models.PROTECT,
                                                     verbose_name='How did you hear about us?')
    # TODO rename these historical_drupal_share_...
    share_with_givewell = models.BooleanField(default=False)
    share_with_gwwc = models.BooleanField(default=False)
    share_with_tlycs = models.BooleanField(default=False)

    # Historical fields from imported data
    drupal_uid = models.IntegerField(default=0, editable=False)
    drupal_username = models.TextField(blank=True, editable=False)
    drupal_preferred_donation_method = models.TextField(blank=True, editable=False)

    @property
    def amount_from_components(self):
        return self.components.aggregate(total=models.Sum('amount'))['total']

    @property
    def partner_charity_str(self):
        num_components = self.components.count()
        if num_components == 1:
            return self.components.get().partner_charity.name
        elif num_components > 1:
            partner_names = [component.partner_charity.name for component in self.components.all()]
            return '{} and {}'.format(', '.join(partner_names[:-1]), partner_names[-1])
        else:
            raise Exception('Pledge does not have any associated components')

    def check_pledge_component_amounts_reconcile(self):
        return self.amount == self.amount_from_components

    def generate_reference(self):
        if self.reference:  # for safety, don't overwrite
            return self.reference
        # TODO
        self.reference = ''.join(random.choice('ABCDEF' + string.digits) for _ in range(12))
        self.save()
        return self.reference

    def save(self, *args, **kwargs):
        if not self.completed_time:
            self.completed_time = timezone.now()
        super(Pledge, self).save(*args, **kwargs)

    def __unicode__(self):
        components = ', '.join([c.__unicode__() for c in self.components.all()])
        return "Pledge of {1} by {0.first_name} {0.last_name}, " \
               "made on {2}. Reference {0.reference}".format(self, components, self.completed_time.date())


class PledgeComponent(models.Model):
    """Tracks the breakdown of a pledge between partner charities"""

    class Meta:
        unique_together = ('pledge', 'partner_charity')

    pledge = models.ForeignKey(Pledge, related_name='components')
    partner_charity = models.ForeignKey(PartnerCharity, related_name='pledge_components')
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0.01)])

    @property
    def proportion(self):
        return self.amount / self.pledge.amount_from_components

    def __unicode__(self):
        return "${0.amount} to {0.partner_charity}".format(self)


# It's possible that we get the reference wrong when a BankTransaction is imported, for example if the donor
# made a typo. The way we correct this is for one of our staff to edit the reference in the admin so that it
# is correct. Therefore, we pay attention here to whether the reference changes and if it does, we delete the
# existing Pledge (if any) and search for a matching one.
class BankTransaction(models.Model):
    date = models.DateField()
    bank_statement_text = models.TextField(blank=True, )
    amount = models.DecimalField(decimal_places=2, max_digits=12, )
    reference = models.TextField(blank=True)
    unique_id = models.TextField(unique=True, editable=False)
    do_not_reconcile = models.BooleanField(default=False)
    pledge = models.ForeignKey(Pledge, blank=True, null=True)
    time_reconciled = models.DateTimeField(blank=True, null=True, editable=False)
    bank_account_id = models.TextField()

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
            self.time_reconciled = timezone.now()
            super(BankTransaction, self).save(*args, **kwargs)
            # Generate a receipt object.
            Receipt.objects.create_from_bank_transaction(self)

    def reconcile(self):
        if self.pledge is None:
            if self.reference:
                # Try to find a matching pledge
                pledges = Pledge.objects.filter(reference=self.reference)
                if len(pledges) > 1:
                    raise Exception("Multiple pledges match. This shouldn't happen.")
                elif len(pledges) == 1:
                    self.pledge = pledges[0]
                    return True

            # Next, try to find a pledge by looking for previously reconciled transactions with identical
            # bank_statement_text.
            earlier_references = BankTransaction.objects.filter(bank_statement_text=self.bank_statement_text,
                                                                pledge__isnull=False,
                                                                ) \
                .exclude(id=self.id) \
                .order_by('reference').distinct('reference') \
                .values_list('reference', flat=True)
            if len(earlier_references) == 1:
                self.reference = earlier_references[0]
                self.pledge = Pledge.objects.get(reference=self.reference)
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

    def save(self, *args, **kwargs):
        super(PinTransaction, self).save(*args, **kwargs)
        if self.succeeded:
            # Let's see how it goes doing this not in celery for now.
            Receipt.objects.create_from_pin_transaction(self)


class Donation(models.Model):
    """Database view with fields common to all donations (BankTransaction, PinTransaction etc.)
    Implemented by creating a view in the database, see
    donation/migrations/0042_amend_donation_view.py.
    """
    # It's convenient for all Donations to have a datetime rather than have bank transactions be a
    # special case because they are received on a particular date, but not a particular time.
    # Bank transactions are therefore assumed received at 6pm on the day they're received, Melbourne time.
    # Reasons for 6pm: 1. this is the usual cut-off time.
    # 2. If you make it midnight it's ambiguous whether at start or end of day
    datetime = models.DateTimeField()
    # Convenient for date to be field even though it's easily calculated from datetime, so you can filter on it
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=12, )
    fees = models.DecimalField(decimal_places=2, max_digits=12, )
    payment_method = models.CharField(max_length=128)
    reference = models.TextField(blank=True)
    pledge = models.ForeignKey(Pledge, blank=True, null=True)
    bank_transaction = models.OneToOneField(BankTransaction, blank=True, null=True)
    pin_transaction = models.OneToOneField(PinTransaction, blank=True, null=True)

    class Meta:
        managed = False

    @property
    def component_summary_str(self):
        return ', '.join('%s ($%s)' % (component.pledge_component.partner_charity.name,
                                       '{0:.2f}'.format(component.amount)
                                       ) for component in self.components.all())


class DonationComponent(models.Model):
    """Database view which calculates the amount donated to each partner charity
    Implemented in donation/migrations/0054_donation_component_view.py
    """
    pledge_component = models.ForeignKey(PledgeComponent, related_name='donation_component')
    donation = models.ForeignKey(Donation, related_name='components')
    amount = models.FloatField()
    fees = models.FloatField()

    class Meta:
        managed = False


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

    def create(self, *args, **kwargs):
        receipt = super(ReceiptManager, self).create(*args, **kwargs)
        from receipts import send_receipt
        send_receipt(receipt)
        return receipt


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
        unique_together = ('date', 'name',)


class XeroReconciledDate(models.Model):
    # Up to and including this date, we take total donation information from xero. After this date, we use the
    # BankTransaction objects. The BankTransaction objects will be missing things like workplace giving.
    date = models.DateField()

    def __unicode__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        super(XeroReconciledDate, self).save(*args, **kwargs)
        # Reload up-to-date data from xero after advancing the date
        # Do it on on user's thread not via celery for obviousness.
        # Lazy imports because circular dependencies
        from tasks import import_trial_balance
        import_trial_balance.delay()


class PartnerCharityReport(models.Model):
    date = models.DateTimeField()
    partner = models.ForeignKey(PartnerCharity)
    time_sent = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        date_until = arrow.get(self.date).shift(days=-1).date()
        return "Report to {0.partner.name} for donations up to and including {1}, sent {0.time_sent}".format(self,
                                                                                                             date_until)


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
