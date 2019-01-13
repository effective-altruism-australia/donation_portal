# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0071_rename_unallocated_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='impact_cost',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='impact_text',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='website',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pledgecomponent',
            name='amount',
            field=models.DecimalField(max_digits=12, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
