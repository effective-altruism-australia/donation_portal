# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations, models
from django.utils import timezone

def set_time_reconciled(apps, schema_editor):
    BankTransaction = apps.get_model('donation', 'BankTransaction')
    for bank_transaction in BankTransaction.objects.filter(pledge__isnull=False, time_reconciled__isnull=True):
        bank_transaction.time_reconciled = timezone.make_aware(datetime(2017, 5, 21), timezone.get_default_timezone())
        bank_transaction.save()


class Migration(migrations.Migration):
    dependencies = [
        ('donation', '0037_eofyreceipt'),
    ]

    operations = [migrations.RunPython(set_time_reconciled),
    ]
