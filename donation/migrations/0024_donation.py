# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0023_create_donation_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('payment_method', models.CharField(max_length=128)),
                ('reference', models.TextField(blank=True)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
