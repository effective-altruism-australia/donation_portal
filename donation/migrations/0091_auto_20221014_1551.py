# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0090_partnercharity_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnercharity',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[('Our recommended charities', 'Our recommended charities'), ('Other charities we support', 'Other charities we support'), ('Help us do more good', 'Help us do more good')]),
        ),
    ]
