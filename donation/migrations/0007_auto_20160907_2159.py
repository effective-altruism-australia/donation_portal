# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_auto_20160907_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='amount',
            field=models.DecimalField(max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='bank_statement_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='date',
            field=models.DateField(),
        ),
    ]
