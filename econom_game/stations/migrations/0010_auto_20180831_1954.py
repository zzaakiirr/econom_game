# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0009_auto_20180831_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='max_bet',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='station',
            name='min_bet',
            field=models.FloatField(),
        ),
    ]