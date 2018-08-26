# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-26 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('card', models.CharField(max_length=25, unique=True)),
                ('pay_pass', models.CharField(max_length=25, unique=True)),
                ('money_amount', models.PositiveIntegerField()),
            ],
        ),
    ]
