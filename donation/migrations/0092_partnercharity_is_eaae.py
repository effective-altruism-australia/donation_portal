# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0091_auto_20221014_1551"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="is_eaae",
            field=models.BooleanField(default=False),
        ),
    ]
