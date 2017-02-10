# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0017_partner_charity_tweaks'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='image_top_margin',
            field=models.IntegerField(default=0, help_text='Can be deleted once we figure out how tocentre the images properly'),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='order_on_website',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partnercharity',
            name='website_label',
            field=models.CharField(help_text='Charity name to display on website', max_length=35),
        ),
    ]
