# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180411_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='add', to='accounts.Address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
