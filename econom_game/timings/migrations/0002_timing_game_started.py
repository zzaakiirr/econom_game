# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timing',
            name='game_started',
            field=models.BooleanField(default=False),
        ),
    ]
