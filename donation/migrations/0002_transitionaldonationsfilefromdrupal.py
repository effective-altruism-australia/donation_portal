# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_squashed_0018_auto_20160915_0432'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransitionalDonationsFileFromDrupal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_uploaded', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=b'')),
            ],
        ),
    ]
