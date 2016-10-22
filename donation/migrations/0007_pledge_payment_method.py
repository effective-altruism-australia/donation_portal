# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_auto_20161022_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='payment_method',
            field=enumfields.fields.EnumField(default=1, max_length=1, enum=donation.models.PaymentMethod),
            preserve_default=False,
        ),
    ]
