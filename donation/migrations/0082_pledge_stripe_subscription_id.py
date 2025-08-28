# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0081_pledge_stripe_checkout_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="pledge",
            name="stripe_subscription_id",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
