# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0075_donation_component_view"),
    ]

    operations = [
        migrations.AddField(
            model_name="banktransaction",
            name="match_future_statement_text",
            field=models.BooleanField(
                default=False,
                help_text='Tick this box if we should link all future transactions with this text to the same pledge. This should only be ticked if the text is reasonably unique. e.g. Do NOT tick it if the text is "donation", or "GiveDirectly" etc.',
            ),
        ),
    ]
