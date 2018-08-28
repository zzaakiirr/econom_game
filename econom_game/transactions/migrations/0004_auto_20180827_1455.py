# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-27 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20180827_1017'),
        ('stations', '0002_auto_20180821_1553'),
        ('transactions', '0003_delete_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='recipient_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='recipient_type',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender_id',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender_type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='stations.Station'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='teams.Team'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='victory',
            field=models.BooleanField(default=False),
        ),
    ]