# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0069_banktransferinstruction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="partnercharity",
            name="order",
        ),
    ]
