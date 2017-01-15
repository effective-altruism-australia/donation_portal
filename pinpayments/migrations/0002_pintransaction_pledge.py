# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0017_partner_charity_tweaks'),
        ('pinpayments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pintransaction',
            name='pledge',
            field=models.ForeignKey(default=1, to='donation.Pledge'),
            preserve_default=False,
        ),
    ]
