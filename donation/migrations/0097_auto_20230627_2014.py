# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0096_auto_20230627_2014"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partnercharity",
            name="slug_id",
            field=models.CharField(
                help_text="Machine readable name (no spaces or special characters)",
                max_length=30,
                unique=True,
                null=True,
                blank=True,
            ),
        ),
    ]
