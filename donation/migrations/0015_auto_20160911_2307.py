# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0014_auto_20160911_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='drupal_preferred_donation_method',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='drupal_uid',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='drupal_username',
            field=models.TextField(editable=False, blank=True),
        ),
    ]
