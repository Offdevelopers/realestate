# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-01 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='property',
            name='latitude',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='longitude',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
