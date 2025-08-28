# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0056_auto_20180525_0039"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
