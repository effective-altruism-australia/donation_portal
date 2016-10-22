# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0005_auto_20161022_0431'),
    ]

    # Start receipt ids at arbitrary high number to avoid collisions with existing receipts
    operations = [
        migrations.RunSQL(
            sql='ALTER SEQUENCE donation_receipt_id_seq RESTART WITH 10000;',
        ),
    ]
