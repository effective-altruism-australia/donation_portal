# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0021_auto_20170215_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='secret',
            field=models.CharField(max_length=16, blank=True),
        ),
    ]
