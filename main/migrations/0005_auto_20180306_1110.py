# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-06 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180306_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='thumbnail',
            field=models.ImageField(upload_to='media'),
        ),
    ]