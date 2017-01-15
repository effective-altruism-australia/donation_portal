# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0016_tweaks_for_frontend_donation_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnercharity',
            name='show_on_website',
            field=models.BooleanField(default=False, help_text='Toggle to add/remove from the website donation page'),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='website_image',
            field=models.ImageField(default='thumbnails/placeholder_image.jpg', help_text='Upload a square image for display on the website', upload_to='thumbnails'),
        ),
        migrations.AddField(
            model_name='partnercharity',
            name='website_label',
            field=models.CharField(default='', help_text='Charity name to display on website', max_length=20),
            preserve_default=False,
        ),
    ]
