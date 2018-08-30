# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-30 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
