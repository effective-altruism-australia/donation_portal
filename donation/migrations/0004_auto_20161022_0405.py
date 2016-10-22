# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0003_auto_20161021_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transitionaldonationsfile',
            name='file',
            field=models.FileField(upload_to=b'uploads/'),
        ),
    ]
