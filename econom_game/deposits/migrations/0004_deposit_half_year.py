# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0003_auto_20180830_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='half_year',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
