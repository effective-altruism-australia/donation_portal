# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0015_auto_20161108_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='first_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='how_did_you_hear_about_us',
            field=enumfields.fields.EnumField(enum=donation.models.HowDidYouHear, max_length=1, blank=True, null=True, verbose_name='How did you hear about us?'),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='last_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='subscribe_to_updates',
            field=models.BooleanField(default=False, verbose_name='Send me latest news and updates'),
        ),
    ]
