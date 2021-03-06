# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-04 19:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180901_0143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operator',
            options={'permissions': (('view_deposit', "Can view '/admin/deposit/' page"), ('view_credit', "Can view '/admin/credit/' page"), ('give_money', "Can view '/admin/give_money/' page"), ('view_confirm_transaction', "Can view '/admin/confirm_transaction/' page"), ('add_group', "Can view '/admin/add_group/' page"))},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('add_station', "Can view '/admin/add_station/' page"), ('add_group', "Can view '/admin/add_group/' page"), ('view_shares', "Can view '/admin/shares/' page"), ('view_confirm_transaction', "Can view '/admin/confirm_transaction/' page"), ('view_give_money', "Can view '/admin/give_money/' page"), ('view_exclude_money', "Can view '/admin/exclude_money/' page"))},
        ),
    ]
