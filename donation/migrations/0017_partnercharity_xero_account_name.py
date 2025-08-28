# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0016_auto_20170126_0946"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="xero_account_name",
            field=models.TextField(
                default="", help_text="Exact text of incoming donation account in xero"
            ),
            preserve_default=False,
        ),
    ]
