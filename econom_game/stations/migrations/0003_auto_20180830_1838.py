# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-30 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_auto_20180821_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
