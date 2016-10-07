# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from decimal import Decimal
import re
import arrow

from django.db import migrations, models
from django.db.models.fields import DecimalField, DateTimeField

# TODO
DRUPAL_CSV_LOCATION = '/share/eaa/donate.csv'

FIELD_MAP = [
    # (django_field_name, drupal_field_name)
    ('id', 'webform_serial'),
    ('completed_time', 'webform_completed_time'),
    ('ip', 'webform_ip_address'),
    ('drupal_uid', 'webform_uid'),
    ('drupal_username', 'webform_username'),
    ('drupal_preferred_donation_method', 'preferred_donation_method'),
    ('reference', 'transactionref'),
    ('recipient_org', 'recipient_org'),
    ('amount', 'donation_amount'),
    ('first_name', 'ea_donor_name'),
    ('last_name', 'ea_donor_last_name'),
    ('email', 'email'),
    ('subscribe_to_updates', 'Subscribe to updates'),
    ('payment_method_text', 'payment_method'),
    ('recurring', 'I want to set up recurring donations through my bank'),
    ('recurring_frequency_text', 'recurring_donation_frequency'),
    ('publish_donation', "Tell the world I've made a donation"),
    ('how_did_you_hear_about_us', 'how_did_you_hear_about_us'),
    ('share_with_givewell',
     'Share my email address and information about my donation with GiveWell. (GiveWell will not share your information with any third parties.)'),
    ('share_with_gwwc',
     'Share my email address and information about my donation with Giving What We Can. (Giving What We Can will not share your information with any third parties.)'),
    ('share_with_tlycs',
     'Share my email address and information about my donation with The Life You Can Save. (The Life You Can Save will not share your information with any third parties.)'),
]


def import_data_from_drupal(apps, schema_editor):
    Pledge = apps.get_model('donation', 'Pledge')
    with open(DRUPAL_CSV_LOCATION, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        # get rid of crap at start
        for row in csv_reader:
            if row and row[0] == 'webform_serial':
                break
        headers = row
        pledges = [dict(zip(headers, row)) for row in csv_reader]

    for pledge in pledges:
        kwargs = {}
        for (django_field, drupal_field) in FIELD_MAP:
            field_type = type(Pledge._meta.get_field_by_name(django_field)[0])

            value = pledge[drupal_field]

            # We only need to manually convert the following fields
            if field_type == DecimalField:
                value = re.sub('[a-zA-Z\$ /,]', '', value)
                value = Decimal(value)
            elif field_type == DateTimeField:
                value = arrow.get(value, 'MM/DD/YYYY - HH:mm').datetime

            kwargs[django_field] = value

        Pledge(**kwargs).save()  # TODO this will create dupes if we have edited the pledge.


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        # migrations.RunPython(import_data_from_drupal),
        # Set id to something high so we don't collide with later imports from drupal
        migrations.RunSQL('ALTER SEQUENCE donation_pledge_id_seq RESTART WITH 10000;')
    ]