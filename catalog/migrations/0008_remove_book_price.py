# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-25 05:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_book_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
    ]
