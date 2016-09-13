# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0016_auto_20160911_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='failed_message',
            field=models.TextField(default=b'', editable=False, blank=True),
        ),
    ]
