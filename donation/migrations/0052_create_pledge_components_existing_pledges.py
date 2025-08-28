# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_pledge_components_for_existing_pledges(apps, schema_editor):
    Pledge = apps.get_model("donation", "Pledge")
    PledgeComponent = apps.get_model("donation", "PledgeComponent")

    for pledge in Pledge.objects.all():
        assert not pledge.pledge_components.exists()
        PledgeComponent.objects.create(
            pledge=pledge, partner_charity=pledge.recipient_org, amount=pledge.amount
        )


def reverse(apps, schema_editor):
    PledgeComponent = apps.get_model("donation", "PledgeComponent")
    PledgeComponent.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("donation", "0051_pledgecomponent"),
    ]

    operations = [
        migrations.RunPython(
            create_pledge_components_for_existing_pledges, reverse_code=reverse
        ),
    ]
