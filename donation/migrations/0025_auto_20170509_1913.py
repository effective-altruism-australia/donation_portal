# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0024_donation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pledge',
            old_name='payment_method',
            new_name='payment_method_old',
        ),
        migrations.RenameField(
            model_name='pledge',
            old_name='recurring_frequency',
            new_name='recurring_frequency_old',
        ),
    ]
