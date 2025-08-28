# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0040_auto_20171204_1349"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pledge",
            name="reference",
            field=models.TextField(blank=True),
        ),
    ]
