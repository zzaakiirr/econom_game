# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-19 22:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180819_2154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stationadmin',
            options={},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('view_station', "Can view '/station' page"),)},
        ),
    ]
