# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-30 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0003_auto_20180830_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]