# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0045_referral_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='order',
            field=models.BigIntegerField(help_text='Enter an integer. Reasons will be ordered from smallest to largest.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='referral',
            name='reason',
            field=models.CharField(help_text='Instead of editing this text, disable this ReferralSource and create a new one.', max_length=256),
        ),
    ]
