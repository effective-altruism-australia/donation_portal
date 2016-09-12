# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0015_auto_20160911_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='receipt_html',
            field=models.TextField(editable=False, blank=True),
        ),
    ]
