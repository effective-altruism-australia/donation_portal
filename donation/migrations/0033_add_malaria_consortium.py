# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_malaria_consortium(apps, schema_editor):
    PartnerCharity = apps.get_model('donation', 'PartnerCharity')
    partner_charities = [{'name': "Malaria Consortium",
                          'email': '@'.join(['info', 'eaa.org.au']),
                          'xero_account_name': "Donations received - Malaria Consortium (250-MC)"},
                         ]

    for partner_charity in partner_charities:
        PartnerCharity(**partner_charity).save()


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0032_auto_20170521_1024'),
    ]

    operations = [
        migrations.RunPython(add_malaria_consortium)
    ]
