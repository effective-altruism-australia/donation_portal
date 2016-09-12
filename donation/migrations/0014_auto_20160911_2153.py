# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0013_remove_banktransaction_pledge2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reconciliation',
            name='bank_transaction',
        ),
        migrations.RemoveField(
            model_name='reconciliation',
            name='pledge',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='reconciliation',
        ),
        migrations.AddField(
            model_name='banktransaction',
            name='pledge',
            field=models.ForeignKey(blank=True, to='donation.Pledge', null=True),
        ),
        migrations.AddField(
            model_name='banktransaction',
            name='time_reconciled',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='bank_transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.BankTransaction', null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='pledge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.Pledge', null=True),
        ),
        migrations.DeleteModel(
            name='Reconciliation',
        ),
    ]
