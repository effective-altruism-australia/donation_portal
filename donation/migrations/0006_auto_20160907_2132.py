# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0005_auto_20160907_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reconciliation',
            name='bank_transaction',
            field=models.OneToOneField(to='donation.BankTransaction'),
        ),
    ]
