from __future__ import unicode_literals

import re

from django.db import models
from django.utils import timezone
from pinpayments.models import PinTransaction as BasePinTransaction

from .pledge import Pledge


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
    match_future_statement_text = models.BooleanField(
        default=False, help_text='Tick this box if we should link all future transactions with this text '
                                 'to the same pledge. This should only be ticked if the text is reasonably unique. '
                                 'e.g. Do NOT tick it if the text is "donation", or "GiveDirectly" etc.')

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
        from .receipt import Receipt
        if self._state.adding:
            self.find_reference_in_bank_statement_text()
        elif self.reference != self._loaded_reference:
            # so that if extra whitespace is entered when copy pasting the reference number, it doesn't matter
            self.reference = self.reference.strip()
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
                                                                pledge__isnull=False, match_future_statement_text=True
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
        from .receipt import Receipt
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

    # def save(self, *args, **kwargs):
    #     super(PinTransaction, self).save(*args, **kwargs)
    #     if self.succeeded:
    #         # Let's see how it goes doing this not in celery for now.
    #         Receipt.objects.create_from_pin_transaction(self)
