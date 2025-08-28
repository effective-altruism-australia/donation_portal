# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0087_donation_component_updated"),
    ]

    operations = [
        migrations.AddField(
            model_name="stripetransaction",
            name="charge_id",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
