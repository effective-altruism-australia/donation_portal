# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0048_auto_20180109_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pledge',
            name='how_did_you_hear_about_us',
        ),
    ]
