# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0079_partnercharity_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='stripe_product_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
