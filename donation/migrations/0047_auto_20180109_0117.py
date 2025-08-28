# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0046_auto_20180109_0115"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Referral",
            new_name="ReferralSource",
        ),
    ]
