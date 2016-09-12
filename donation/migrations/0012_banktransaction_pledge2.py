# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0011_auto_20160911_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='pledge2',
            field=models.ForeignKey(blank=True, to='donation.Pledge', null=True),
        ),
    ]
