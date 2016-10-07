# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'donation', '0001_initial'), (b'donation', '0002_import_pledges_from_drupal'), (b'donation', '0003_banktransaction'), (b'donation', '0004_auto_20160907_2107'), (b'donation', '0005_auto_20160907_2131'), (b'donation', '0006_auto_20160907_2132'), (b'donation', '0007_auto_20160907_2159'), (b'donation', '0008_auto_20160907_2310'), (b'donation', '0009_auto_20160908_0015'), (b'donation', '0010_auto_20160911_2015'), (b'donation', '0011_auto_20160911_2032'), (b'donation', '0012_banktransaction_pledge2'), (b'donation', '0013_remove_banktransaction_pledge2'), (b'donation', '0014_auto_20160911_2153'), (b'donation', '0015_auto_20160911_2307'), (b'donation', '0016_auto_20160911_2320'), (b'donation', '0017_receipt_failed_message'), (b'donation', '0018_auto_20160915_0432')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed_time', models.DateTimeField()),
                ('ip', models.GenericIPAddressField()),
                ('reference', models.TextField()),
                ('recipient_org', models.TextField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('subscribe_to_updates', models.BooleanField(default=False)),
                ('payment_method_text', models.TextField(blank=True)),
                ('recurring', models.BooleanField()),
                ('recurring_frequency_text', models.TextField(blank=True)),
                ('publish_donation', models.BooleanField(default=False)),
                ('how_did_you_hear_about_us', models.TextField(blank=True)),
                ('share_with_givewell', models.BooleanField(default=False)),
                ('share_with_gwwc', models.BooleanField(default=False)),
                ('share_with_tlycs', models.BooleanField(default=False)),
                ('drupal_uid', models.IntegerField(default=0)),
                ('drupal_username', models.TextField(blank=True)),
                ('drupal_preferred_donation_method', models.TextField(blank=True)),
            ],
        ),
        migrations.RunSQL(
            sql='ALTER SEQUENCE donation_pledge_id_seq RESTART WITH 10000;',
        ),
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('bank_statement_text', models.TextField(blank=True)),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('reference', models.TextField(blank=True)),
                ('unique_id', models.TextField(unique=True, editable=False)),
                ('its_not_a_donation', models.BooleanField(default=False)),
                ('pledge', models.ForeignKey(blank=True, to='donation.Pledge', null=True)),
                ('time_reconciled', models.DateTimeField(null=True, editable=False, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_sent', models.DateTimeField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('receipt_html', models.TextField(editable=False, blank=True)),
                ('bank_transaction', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.BankTransaction', null=True)),
                ('pledge', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='donation.Pledge', null=True)),
                ('failed_message', models.TextField(default=b'', editable=False, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pledge',
            name='drupal_preferred_donation_method',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='drupal_uid',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='drupal_username',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('name', models.TextField()),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('ytd_amount', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='XeroReconciledDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('date', 'name')]),
        ),
    ]
