from __future__ import unicode_literals

import arrow
from django.db import models

from .partner_charity import PartnerCharity


class PartnerCharityReport(models.Model):
    date = models.DateTimeField()
    partner = models.ForeignKey(PartnerCharity, on_delete=models.CASCADE)
    time_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date_until = arrow.get(self.date).shift(days=-1).date()
        return "Report to {0.partner.name} for donations up to and including {1}, sent {0.time_sent}".format(self,
                                                                                                             date_until)
