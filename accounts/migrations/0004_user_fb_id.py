# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-03 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_socialprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fb_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
