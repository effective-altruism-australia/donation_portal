# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0084_stripetransaction_payment_intent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='stripe_customer_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stripetransaction',
            name='customer_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
