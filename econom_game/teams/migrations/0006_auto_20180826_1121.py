# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-26 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20180826_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='bank',
            field=models.PositiveIntegerField(),
        ),
    ]
