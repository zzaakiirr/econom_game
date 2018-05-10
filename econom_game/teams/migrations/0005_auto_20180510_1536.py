# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-10 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20180510_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='team',
        ),
        migrations.AddField(
            model_name='team',
            name='card',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='card', to='teams.Card'),
        ),
    ]
