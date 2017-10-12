# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0038_set_time_reconciled_on_all_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='how_did_you_hear_about_us',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='How did you hear about us?', choices=[('The Life You Can Save', 'The Life You Can Save'), ('News', 'News'), ('Advertising', 'Advertising'), ('GiveWell', 'GiveWell'), ('From the charity (SCI, Evidence Action, GiveDirectly)', 'From the charity (SCI, Evidence Action, GiveDirectly)'), ('Search engine (Google etc.)', 'Search engine (Google etc.)'), ('Friend', 'Friend'), ('Giving What We Can', 'Giving What We Can'), ("Ezra Justin's Bar-mitzvah", "Ezra Justin's Bar-mitzvah")]),
        ),
    ]
