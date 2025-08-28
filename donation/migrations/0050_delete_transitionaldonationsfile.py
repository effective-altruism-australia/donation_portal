# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0049_remove_pledge_how_did_you_hear_about_us"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TransitionalDonationsFile",
        ),
    ]
