# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fill_in_xero_account_names_for_partner_charities(apps, schema_editor):
    PartnerCharity = apps.get_model('donation', 'PartnerCharity')

    partner_charities = [{'name': "Schistosomiasis Control Initiative",
                          'xero': "Donations received - Schistosomiasis Control Initiative (SCI) (250-SCI)"},
                         {'name': "GiveDirectly",
                          'xero': "Donations received - GiveDirectly (250-GD)"},
                         {'name': "GiveDirectly Basic income research",
                          'xero': "Donations received - GiveDirectly Basic Income Research (250-GDBI)"},
                         {'name': "Deworm the World Initiative (led by Evidence Action)",
                          'xero': "Donations received - Deworm the World Initiative (Evidence Action) (250-DWTW)"},
                         ]

    for partner_charity in partner_charities:
        pc = PartnerCharity.objects.get(name=partner_charity['name'])
        pc.xero_account_name = partner_charity['xero']
        pc.save()


class Migration(migrations.Migration):
    dependencies = [
        ('donation', '0017_partnercharity_xero_account_name'),
    ]

    operations = [
        migrations.RunPython(fill_in_xero_account_names_for_partner_charities)
    ]
