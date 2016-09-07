# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed_time', models.DateTimeField()),
                ('ip', models.GenericIPAddressField()),
                ('reference', models.TextField()),
                ('recipient_org', models.TextField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('subscribe_to_updates', models.BooleanField(default=False)),
                ('payment_method_text', models.TextField(blank=True)),
                ('recurring', models.BooleanField()),
                ('recurring_frequency_text', models.TextField(blank=True)),
                ('publish_donation', models.BooleanField(default=False)),
                ('how_did_you_hear_about_us', models.TextField(blank=True)),
                ('share_with_givewell', models.BooleanField(default=False)),
                ('share_with_gwwc', models.BooleanField(default=False)),
                ('share_with_tlycs', models.BooleanField(default=False)),
                ('drupal_uid', models.IntegerField(default=0)),
                ('drupal_username', models.TextField(blank=True)),
                ('drupal_preferred_donation_method', models.TextField(blank=True)),
            ],
        ),
    ]
