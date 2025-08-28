# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0010_auto_20161022_2119"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="email",
            field=models.EmailField(
                default="info@eaa.org.au",
                help_text="Used to cc the charity on receipts",
                max_length=254,
            ),
            preserve_default=False,
        ),
    ]
