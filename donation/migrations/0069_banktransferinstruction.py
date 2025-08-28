# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0068_auto_20180612_2016"),
    ]

    operations = [
        migrations.CreateModel(
            name="BankTransferInstruction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("time_sent", models.DateTimeField(null=True, blank=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "failed_message",
                    models.TextField(default="", editable=False, blank=True),
                ),
                (
                    "pledge",
                    models.OneToOneField(
                        to="donation.Pledge", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
    ]
