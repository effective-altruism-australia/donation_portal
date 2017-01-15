# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0018_auto_20170210_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='website_description',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]
