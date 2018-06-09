# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0059_auto_20180606_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='thumbnail',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
