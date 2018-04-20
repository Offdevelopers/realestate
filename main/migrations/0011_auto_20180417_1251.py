# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_property_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='community',
            field=models.CharField(choices=[('Rural', 'Rural'), ('Urban', 'Urban')], default='Rural', max_length=50),
        ),
        migrations.AddField(
            model_name='property',
            name='stories',
            field=models.IntegerField(default=2),
        ),
    ]