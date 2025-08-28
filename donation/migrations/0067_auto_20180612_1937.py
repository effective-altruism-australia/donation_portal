# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def trim_names(apps, schema_editor):
    Pledge = apps.get_model("donation", "Pledge")
    for pledge in Pledge.objects.all():
        pledge.first_name = pledge.first_name[0:100]
        pledge.last_name = pledge.last_name[0:100]
        pledge.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("donation", "0066_auto_20180611_2210"),
    ]

    operations = [
        migrations.RunPython(trim_names, reverse_code=reverse),
        migrations.AlterField(
            model_name="pledge",
            name="first_name",
            field=models.CharField(max_length=100, verbose_name="name", blank=True),
        ),
        migrations.AlterField(
            model_name="pledge",
            name="last_name",
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
