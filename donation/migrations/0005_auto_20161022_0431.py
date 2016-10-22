# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0004_auto_20161022_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
