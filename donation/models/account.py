from __future__ import unicode_literals

from django.db import models


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
        from donation.eaaxero import import_trial_balance
        import_trial_balance.delay()
