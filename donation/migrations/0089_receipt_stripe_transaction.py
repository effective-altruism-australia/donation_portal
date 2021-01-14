# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0088_stripetransaction_charge_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='stripe_transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.StripeTransaction', null=True),
        ),
    ]
