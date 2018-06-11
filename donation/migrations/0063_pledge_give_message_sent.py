# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0062_auto_20180611_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='give_message_sent',
            field=models.BooleanField(default=False),
        ),
    ]
