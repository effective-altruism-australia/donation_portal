# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0058_referralsource_slug_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='amount',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2),
        ),
    ]
