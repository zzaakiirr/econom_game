# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-15 17:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20180512_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999)]),
        ),
    ]
