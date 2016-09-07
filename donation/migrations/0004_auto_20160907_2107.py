# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0003_banktransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_sent', models.DateTimeField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Reconciliation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('automatically_reconciled', models.BooleanField(default=False)),
                ('bank_transaction', models.ForeignKey(to='donation.BankTransaction')),
                ('pledge', models.ForeignKey(to='donation.Pledge')),
            ],
        ),
        migrations.AddField(
            model_name='receipt',
            name='transaction',
            field=models.ForeignKey(to='donation.Reconciliation'),
        ),
    ]
