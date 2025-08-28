# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0097_auto_20230627_2014"),
    ]

    operations = [
        migrations.AddField(
            model_name="eofyreceipt",
            name="is_eaae",
            field=models.BooleanField(default=False),
        ),
    ]
