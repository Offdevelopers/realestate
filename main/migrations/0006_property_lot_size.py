# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-07 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180306_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='lot_size',
            field=models.IntegerField(default=2000),
        ),
    ]