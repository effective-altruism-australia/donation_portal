# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0052_create_pledge_components_existing_pledges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='recipient_org',
            field=models.ForeignKey(to='donation.PartnerCharity', null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='pledgecomponent',
            unique_together=set([('pledge', 'partner_charity')]),
        ),
    ]
