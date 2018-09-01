# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 23:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180831_2313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='financier',
            options={'permissions': (('view_shares', "Can view '/admin/shares/' page"),)},
        ),
        migrations.AlterModelOptions(
            name='operator',
            options={'permissions': (('view_deposit', "Can view '/admin/deposit/' page"), ('view_credit', "Can view '/admin/credit/' page"))},
        ),
    ]