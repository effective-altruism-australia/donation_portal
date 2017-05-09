# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0025_auto_20170509_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='payment_method',
            field=enumfields.fields.EnumIntegerField(default=2, enum=donation.models.PaymentMethod),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pledge',
            name='recurring_frequency',
            field=enumfields.fields.EnumIntegerField(blank=True, null=True, enum=donation.models.RecurringFrequency),
        ),
    ]
