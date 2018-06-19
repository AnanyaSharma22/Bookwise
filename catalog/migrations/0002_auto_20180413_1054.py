# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-13 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='title',
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/'),
        ),
    ]
