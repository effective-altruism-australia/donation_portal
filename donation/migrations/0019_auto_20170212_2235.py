# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinpayments', '0001_initial'),
        ('donation', '0018_auto_20170126_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='PinTransaction',
            fields=[
                ('pintransaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pinpayments.PinTransaction', on_delete=models.CASCADE)),
            ],
            bases=('pinpayments.pintransaction',),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='first_name',
            field=models.CharField(max_length=1024, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='how_did_you_hear_about_us',
            field=models.TextField(blank=True, null=True, verbose_name='How did you hear about us?', choices=[('The Life You Can Save', 'The Life You Can Save'), ('News', 'News'), ('Advertising', 'Advertising'), ('GiveWell', 'GiveWell'), ('From the charity (SCI, Evidence Action, GiveDirectly)', 'From the charity (SCI, Evidence Action, GiveDirectly)'), ('Search engine (Google etc.)', 'Search engine (Google etc.)'), ('Friend', 'Friend'), ('Giving What We Can', 'Giving What We Can')]),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='last_name',
            field=models.CharField(max_length=1024, blank=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='subscribe_to_updates',
            field=models.BooleanField(default=False, verbose_name='Send me latest news and updates'),
        ),
        migrations.AddField(
            model_name='pintransaction',
            name='pledge',
            field=models.ForeignKey(to='donation.Pledge', on_delete=models.CASCADE),
        ),
    ]
