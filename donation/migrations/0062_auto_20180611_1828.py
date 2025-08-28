# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0061_auto_20180609_1817"),
    ]

    operations = [
        migrations.AddField(
            model_name="pledge",
            name="gift_personal_message",
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="pledge",
            name="gift_recipient_email",
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="pledge",
            name="gift_recipient_name",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="pledge",
            name="is_gift",
            field=models.BooleanField(default=False),
        ),
    ]
