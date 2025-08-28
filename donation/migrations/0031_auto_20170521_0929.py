# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0030_partnercharityreport_time_sent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partnercharityreport",
            name="date",
            field=models.DateTimeField(),
        ),
    ]
