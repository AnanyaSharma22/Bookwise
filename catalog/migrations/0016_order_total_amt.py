# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_auto_20180426_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amt',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
