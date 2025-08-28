# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0055_auto_20180514_2112"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="order",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="partnercharity",
            name="slug_id",
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name="partnercharity",
            name="name",
            field=models.TextField(unique=True, verbose_name="Name (human readable)"),
        ),
    ]
