# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0008_auto_20161022_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='recipient_org',
            field=models.ForeignKey(default=1, to='donation.PartnerCharity'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partnercharity',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
