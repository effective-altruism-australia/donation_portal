# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0017_receipt_failed_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('name', models.TextField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('ytd_amount', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='XeroReconciledDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('date', 'name')]),
        ),
    ]
