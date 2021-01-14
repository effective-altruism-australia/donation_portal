# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0083_auto_20210102_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripetransaction',
            name='payment_intent_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
