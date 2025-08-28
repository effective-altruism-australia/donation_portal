# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0028_auto_20170509_1943"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnerCharityReport",
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
                ("date", models.DateField()),
                (
                    "partner",
                    models.ForeignKey(
                        to="donation.PartnerCharity", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
    ]
