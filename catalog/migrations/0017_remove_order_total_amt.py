# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_order_total_amt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_amt',
        ),
    ]