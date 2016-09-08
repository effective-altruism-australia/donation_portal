# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0008_auto_20160907_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='receipt_html',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='time_sent',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
