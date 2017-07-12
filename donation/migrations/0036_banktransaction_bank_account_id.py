# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0035_amend_donation_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='bank_account_id',
            field=models.TextField(default=settings.XERO_INCOMING_ACCOUNT_ID),
            preserve_default=False,
        ),
    ]
