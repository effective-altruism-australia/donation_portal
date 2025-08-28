# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0065_add_unallocated_and_eaa_partner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partnercharity",
            name="order",
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
