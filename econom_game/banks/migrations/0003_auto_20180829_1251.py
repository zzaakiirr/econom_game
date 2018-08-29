# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-29 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0002_credit_deposit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='credit',
            name='team',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='team',
        ),
        migrations.DeleteModel(
            name='Credit',
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
    ]