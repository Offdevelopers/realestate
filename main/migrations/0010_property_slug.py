# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-17 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]