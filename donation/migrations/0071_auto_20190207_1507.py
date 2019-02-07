# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0070_remove_partnercharity_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='match_future_statement_text',
            field=models.BooleanField(default=False, help_text='Tick this box if we should link all future transactions with this text to the same pledge'),
        ),
        migrations.AlterField(
            model_name='pledgecomponent',
            name='amount',
            field=models.DecimalField(max_digits=12, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
