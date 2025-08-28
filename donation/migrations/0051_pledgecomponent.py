# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0050_delete_transitionaldonationsfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="PledgeComponent",
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
                ("amount", models.DecimalField(max_digits=12, decimal_places=2)),
                (
                    "partner_charity",
                    models.ForeignKey(
                        related_name="pledge_components",
                        to="donation.PartnerCharity",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "pledge",
                    models.ForeignKey(
                        related_name="pledge_components",
                        to="donation.Pledge",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
    ]
