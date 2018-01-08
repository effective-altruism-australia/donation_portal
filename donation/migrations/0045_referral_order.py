# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0044_referral_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='order',
            field=models.BigIntegerField(help_text='Enter an integer. Reasons will be ordered fromsmallest to largest.', null=True, blank=True),
        ),
    ]
