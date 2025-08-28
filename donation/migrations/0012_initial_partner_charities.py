# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_initial_partner_charities(apps, schema_editor):
    PartnerCharity = apps.get_model("donation", "PartnerCharity")
    partner_charities = [
        {
            "name": "Schistosomiasis Control Initiative",
            "email": "@".join(["schisto", "imperial.ac.uk"]),
        },
        {"name": "GiveDirectly", "email": "@".join(["info", "givedirectly.org"])},
        {
            "name": "GiveDirectly Basic income research",
            "email": "@".join(["info", "givedirectly.org"]),
        },
        {
            "name": "Deworm the World Initiative (led by Evidence Action)",
            "email": "@".join(["info", "evidenceaction.org"]),
        },
    ]

    for partner_charity in partner_charities:
        PartnerCharity(**partner_charity).save()


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0011_partnercharity_email"),
    ]

    operations = [migrations.RunPython(add_initial_partner_charities)]
