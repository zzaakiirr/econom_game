# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 23:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_financier_operator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('add_station', "Can view '/admin/add_station/' page"), ('add_group', "Can view '/admin/add_group/' page"), ('view_shares', "Can view '/admin/shares/' page"), ('confirm_transaction', "Can view '/admin/confirm_transaction/' page"), ('give_money', "Can view '/admin/give_money/' page"), ('exclude_money', "Can view '/admin/exclude_money/' page"))},
        ),
    ]
