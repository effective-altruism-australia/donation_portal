# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_transitionaldonationsfilefromdrupal'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TransitionalDonationsFileFromDrupal',
            new_name='TransitionalDonationsFile',
        ),
    ]
