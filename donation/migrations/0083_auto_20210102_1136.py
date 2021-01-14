# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0082_pledge_stripe_subscription_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('date', models.DateField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('fees', models.DecimalField(max_digits=12, decimal_places=2)),
                ('reference', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='pledge',
            name='stripe_payment_intent_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stripetransaction',
            name='pledge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='donation.Pledge', null=True),
        ),
    ]
