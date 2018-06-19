# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 10:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_remove_orderdetail_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.TimeField(default='15:51:42'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('dispatched', 'dispatched'), ('delivered', 'Delivered')], default='dispatched', max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='stripe_cust_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
