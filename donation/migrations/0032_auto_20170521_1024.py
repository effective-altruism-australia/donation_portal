# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    def add_missing_references(apps, schema_editor):
        BankTransaction = apps.get_model("donation", "BankTransaction")

        for bt in BankTransaction.objects.filter(reference="", pledge__isnull=False):
            bt.reference = bt.pledge.reference
            super(BankTransaction, bt).save()

    dependencies = [
        ("donation", "0031_auto_20170521_0929"),
    ]

    operations = [migrations.RunPython(add_missing_references)]
