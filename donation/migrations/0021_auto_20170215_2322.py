# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0020_auto_20170213_1952"),
    ]

    operations = [
        migrations.AddField(
            model_name="receipt",
            name="pin_transaction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="donation.PinTransaction",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="pledge",
            name="first_name",
            field=models.CharField(max_length=1024, verbose_name="name", blank=True),
        ),
    ]
