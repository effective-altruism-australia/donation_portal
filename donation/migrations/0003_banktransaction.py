# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_import_pledges_from_drupal'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(editable=False)),
                ('bank_statement_text', models.TextField(editable=False, blank=True)),
                ('amount', models.DecimalField(editable=False, max_digits=12, decimal_places=2)),
                ('reference', models.TextField(blank=True)),
                ('unique_id', models.TextField(unique=True, editable=False)),
            ],
        ),
    ]
