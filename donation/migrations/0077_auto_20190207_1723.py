# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0076_banktransaction_match_future_statement_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="email_cc",
            field=models.EmailField(
                help_text="Cced on partner charity reports",
                max_length=254,
                null=True,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="partnercharity",
            name="email",
            field=models.EmailField(
                help_text="Used to send the partner charity reports", max_length=254
            ),
        ),
    ]
