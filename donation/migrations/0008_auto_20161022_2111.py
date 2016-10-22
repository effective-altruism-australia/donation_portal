# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import enumfields.fields
import donation.models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0007_pledge_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerCharity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='payment_method_text',
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='recurring_frequency_text',
        ),
        migrations.AddField(
            model_name='pledge',
            name='recurring_frequency',
            field=enumfields.fields.EnumField(default=1, max_length=1, enum=donation.models.RecurringFrequency),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='recipient_org',
        ),
    ]
