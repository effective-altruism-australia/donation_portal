from __future__ import unicode_literals

from django.db import models

from .pledge import Pledge, PledgeComponent
from .transaction import BankTransaction, PinTransaction


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
