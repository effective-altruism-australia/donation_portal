# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0060_partnercharity_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pledge',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='recipient_org',
        ),
    ]
