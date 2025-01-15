# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0054_donation_component_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('fees', models.FloatField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='pledgecomponent',
            name='amount',
            field=models.DecimalField(max_digits=12, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='pledgecomponent',
            name='pledge',
            field=models.ForeignKey(related_name='components', to='donation.Pledge', on_delete=models.CASCADE),
        ),
    ]
