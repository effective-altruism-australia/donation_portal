# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0012_initial_partner_charities'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partnercharity',
            options={'verbose_name_plural': 'Partner charities'},
        ),
        migrations.AlterField(
            model_name='pledge',
            name='recurring_frequency',
            field=enumfields.fields.EnumField(blank=True, max_length=1, null=True, enum=donation.models.RecurringFrequency),
        ),
    ]
