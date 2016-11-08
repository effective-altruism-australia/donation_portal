# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0014_auto_20161029_0728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransaction',
            old_name='its_not_a_donation',
            new_name='do_not_reconcile',
        ),
    ]
