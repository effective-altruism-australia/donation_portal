# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0078_auto_20200225_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='ordering',
            field=models.IntegerField(default=1),
        ),
    ]
