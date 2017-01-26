# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0015_auto_20161108_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xeroreconcileddate',
            name='date',
            field=models.DateField(),
        ),
    ]
