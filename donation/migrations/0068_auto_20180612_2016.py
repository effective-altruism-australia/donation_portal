# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0067_auto_20180612_1937"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pledge",
            old_name="give_message_sent",
            new_name="gift_message_sent",
        ),
    ]
