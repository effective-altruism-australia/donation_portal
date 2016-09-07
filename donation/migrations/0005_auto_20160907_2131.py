# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donation', '0004_auto_20160907_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='its_a_transfer_not_a_donation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='time_reconciled',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 7, 21, 31, 10, 544269), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reconciliation',
            name='user_who_manually_reconciled',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='reconciliation',
            name='bank_transaction',
            field=models.ForeignKey(to='donation.BankTransaction', unique=True),
        ),
    ]
