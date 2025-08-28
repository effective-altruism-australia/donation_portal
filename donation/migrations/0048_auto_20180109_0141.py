# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0047_auto_20180109_0117"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referralsource",
            name="reason",
            field=models.CharField(
                help_text="Instead of editing this text, you probably want to disable this ReferralSource and create a new one. If you edit this, you'll also update the referral sources for donations already made.",
                unique=True,
                max_length=256,
            ),
        ),
    ]
