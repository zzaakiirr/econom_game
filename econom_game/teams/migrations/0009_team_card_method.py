# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-26 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_delete_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='card_method',
            field=models.CharField(default=None, max_length=25),
            preserve_default=False,
        ),
    ]