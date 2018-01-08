# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def copy_existing_referrals_into_new_field(apps, schema_editor):
    Pledge = apps.get_model('donation', 'Pledge')
    Referral = apps.get_model('donation', 'Referral')
    reasons = Pledge.objects.values_list('how_did_you_hear_about_us', flat=True).distinct()
    for reason in reasons:
        if reason:  # Filter out None and u''
            Referral.objects.create(reason=reason)

    for pledge in Pledge.objects.all():
        reason = pledge.how_did_you_hear_about_us
        if reason:
            pledge.how_did_you_hear_about_us_db = Referral.objects.get(reason=reason)
            pledge.save()


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0042_amend_donation_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='pledge',
            name='how_did_you_hear_about_us_db',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='How did you hear about us?', blank=True, to='donation.Referral', null=True),
        ),
        migrations.RunPython(copy_existing_referrals_into_new_field)
    ]
