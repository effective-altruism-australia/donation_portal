# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0007_auto_20160907_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='transaction',
            new_name='reconciliation',
        ),
    ]
