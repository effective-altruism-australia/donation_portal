# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0077_auto_20190207_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='connect_to_community',
            field=models.BooleanField(default=False, verbose_name='Connect me with my local Effective Altruism community'),
        ),
        migrations.AddField(
            model_name='pledge',
            name='country',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pledge',
            name='postcode',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pledge',
            name='subscribe_to_newsletter',
            field=models.BooleanField(default=False, verbose_name='Subscribe me to the global Effective Altruism newsletter'),
        ),
    ]
