# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

mapping = {'Schistosomiasis Control Initiative': ('sci', 'logo_sci.jpg'),
             'GiveDirectly':('give-directly', 'logo_givedirectly.png'),
             'GiveDirectly Basic income research': ('gd-basic-income', 'logo_gdbi.png'),
             'Malaria Consortium': ('malaria-consortium', 'logo_mc.jpg'),
             'Deworm the World Initiative (led by Evidence Action)': ('de-worm', 'logo_evidenceaction.gif')}


def create_partner_charity_slugs(apps, schema_editor):
    PartnerCharity = apps.get_model('donation', 'PartnerCharity')
    for partner_charity in PartnerCharity.objects.all():
        if partner_charity.name in mapping:
            slug, thumbnail = mapping[partner_charity.name]
            if partner_charity.slug_id is None:
                partner_charity.slug_id, = slug
                partner_charity.save()
            if partner_charity.thumbnail is None:
                partner_charity.thumbnail = 'thumbnails/%s' % thumbnail
                partner_charity.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('donation', '0063_pledge_give_message_sent'),
    ]

    operations = [
        migrations.RunPython(create_partner_charity_slugs,
                             reverse_code=reverse),
    ]
