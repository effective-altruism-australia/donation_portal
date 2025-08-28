# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import donation.models.partner_charity


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0072_auto_20190113_1114"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partnercharity",
            name="impact_cost",
            field=models.FloatField(
                help_text="Total impact will be calculated as donation amount divided by impact cost",
                null=True,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="partnercharity",
            name="impact_text",
            field=models.CharField(
                blank=True,
                max_length=500,
                null=True,
                validators=[donation.models.partner_charity.validate_impact_text],
            ),
        ),
    ]
