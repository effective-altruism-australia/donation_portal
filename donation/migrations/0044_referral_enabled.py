# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0043_auto_20180109_0012"),
    ]

    operations = [
        migrations.AddField(
            model_name="referral",
            name="enabled",
            field=models.BooleanField(default=True),
        ),
    ]
