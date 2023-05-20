# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0093_pledge_is_eaae'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='is_eaae',
            field=models.BooleanField(default=False),
        ),
    ]
