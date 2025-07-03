# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import json


class Migration(migrations.Migration):

    def add_partner_charity_data(apps, schema_editor):
        PartnerCharity = apps.get_model('donation', 'PartnerCharity')

        for charity in json.loads(open('donation/migrations/0074_charity_data.json', 'r', encoding='utf-8').read()):
            partners = PartnerCharity.objects.filter(slug_id=charity['slug_id'])
            if not partners.exists():
                continue
            else:
                partner = partners.get()
                partner.bio = charity['bio']
                partner.impact_text = charity['impact_text']
                partner.website = charity['website']
                partner.impact_cost = charity['impact_cost']
                partner.save()

    def add_partner_charity_data_reverse(apps, schema_editor):
        pass

    dependencies = [
        ('donation', '0073_auto_20190113_1216'),
    ]

    operations = [
        migrations.RunPython(add_partner_charity_data, reverse_code=add_partner_charity_data_reverse)
    ]
