# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-30 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20180826_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
