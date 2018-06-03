# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0057_partnercharity_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralsource',
            name='slug_id',
            field=models.CharField(max_length=30, unique=True, null=True),
        ),
    ]
