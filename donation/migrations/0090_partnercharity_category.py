# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0089_receipt_stripe_transaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnercharity",
            name="category",
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
