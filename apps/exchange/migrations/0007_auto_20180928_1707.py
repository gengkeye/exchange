# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-28 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='buy_currency',
            field=models.CharField(choices=[('CNY', 'CNY'), ('PHP', 'PHP'), ('USD', 'USD'), ('TWD', 'TWD')], max_length=30),
        ),
        migrations.AlterField(
            model_name='bid',
            name='sell_currency',
            field=models.CharField(choices=[('CNY', 'CNY'), ('PHP', 'PHP'), ('USD', 'USD'), ('TWD', 'TWD')], max_length=30),
        ),
    ]
