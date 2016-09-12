# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0009_auto_20160908_0015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransaction',
            old_name='its_a_transfer_not_a_donation',
            new_name='its_not_a_donation',
        ),
        migrations.RemoveField(
            model_name='reconciliation',
            name='automatically_reconciled',
        ),
        migrations.RemoveField(
            model_name='reconciliation',
            name='user_who_manually_reconciled',
        ),
        migrations.AlterField(
            model_name='receipt',
            name='reconciliation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.Reconciliation', null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='time_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reconciliation',
            name='bank_transaction',
            field=models.OneToOneField(related_name='reconciliation', to='donation.BankTransaction'),
        ),
    ]
