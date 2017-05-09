# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0027_migrate_enums'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='payment_method_old',
            field=enumfields.fields.EnumField(blank=True, max_length=1, null=True, enum=donation.models.PaymentMethod),
        ),
    ]
