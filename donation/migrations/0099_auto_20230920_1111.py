# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0098_eofyreceipt_is_eaae'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='stripetransaction',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]