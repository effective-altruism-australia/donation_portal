from __future__ import unicode_literals

from django.db import models

from .pledge import Pledge


class BankTransferInstruction(models.Model):
    time_sent = models.DateTimeField(blank=True, null=True)
    pledge = models.OneToOneField(Pledge, on_delete=models.CASCADE)
    # The email on the pledge might get edited, so let's record the one we used here.
    email = models.EmailField()
    failed_message = models.TextField(blank=True, editable=False, default='')

    @property
    def sent(self):
        return self.time_sent is not None

    @property
    def failed(self):
        return self.failed_message != ''
