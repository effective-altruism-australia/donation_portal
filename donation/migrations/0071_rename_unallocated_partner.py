# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def rename_unallocated(apps, schema_editor):
    PartnerCharity = apps.get_model('donation', 'PartnerCharity')
    PartnerCharity.objects.update_or_create(
        slug_id='unallocated',
        defaults={
            'email': 'info@eaa.org.au',
            'name': 'our partner charities',
            'active': False
        }
    )


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('donation', '0070_remove_partnercharity_order'),
    ]

    operations = [
        migrations.RunPython(rename_unallocated,
                             reverse_code=reverse),
    ]
