# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0029_partnercharityreport"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharityreport",
            name="time_sent",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2017, 5, 20, 22, 42, 52, 773891, tzinfo=timezone.utc
                ),
                auto_now_add=True,
            ),
            preserve_default=False,
        ),
    ]
