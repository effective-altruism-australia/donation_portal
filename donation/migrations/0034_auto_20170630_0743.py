# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0033_add_malaria_consortium'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pledge',
            name='payment_method_old',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='recurring_frequency_old',
        ),
    ]
