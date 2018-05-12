# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-12 09:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('cvv', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('money_amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=25)),
                ('login', models.CharField(max_length=25)),
                ('card', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='card', to='teams.Card')),
            ],
        ),
    ]
