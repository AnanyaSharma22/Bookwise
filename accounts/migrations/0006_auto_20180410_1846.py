# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-10 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180410_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=70, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=70, verbose_name='country'),
        ),
    ]