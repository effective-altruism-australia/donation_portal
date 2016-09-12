# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0012_banktransaction_pledge2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banktransaction',
            name='pledge2',
        ),
    ]
