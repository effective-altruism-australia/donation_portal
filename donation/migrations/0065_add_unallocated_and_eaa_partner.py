# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_eaa_and_unallocated(apps, schema_editor):
    PartnerCharity = apps.get_model("donation", "PartnerCharity")
    PartnerCharity.objects.update_or_create(
        slug_id="eaa",
        defaults={
            "email": "info@eaa.org.au",
            "name": "Effective Altruism Australia",
            "active": False,
        },
    )
    PartnerCharity.objects.update_or_create(
        slug_id="unallocated",
        defaults={"email": "info@eaa.org.au", "name": "Unallocated", "active": False},
    )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("donation", "0064_add_partner_charity_slug_ids"),
    ]

    operations = [
        migrations.RunPython(create_eaa_and_unallocated, reverse_code=reverse),
    ]
