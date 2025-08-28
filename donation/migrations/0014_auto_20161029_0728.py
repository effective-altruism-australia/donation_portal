# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0013_auto_20161022_2200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="date",
            field=models.DateField(),
        ),
    ]
