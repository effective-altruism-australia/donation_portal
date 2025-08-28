# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0026_auto_20170509_1922"),
    ]

    operations = [
        migrations.RunSQL(
            """
        UPDATE donation_pledge
            SET payment_method = payment_method_old::int,
                recurring_frequency = recurring_frequency_old::int;
    """
        )
    ]
