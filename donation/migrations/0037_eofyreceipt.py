# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0036_banktransaction_bank_account_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="EOFYReceipt",
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
                ("email", models.EmailField(max_length=254)),
                ("year", models.IntegerField()),
                ("time_sent", models.DateTimeField(auto_now_add=True)),
                ("receipt_html_page_1", models.TextField(editable=False, blank=True)),
                ("receipt_html_page_2", models.TextField(editable=False, blank=True)),
                (
                    "failed_message",
                    models.TextField(default="", editable=False, blank=True),
                ),
            ],
        ),
    ]
