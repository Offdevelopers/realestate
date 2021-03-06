# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-15 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20180615_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='apperance',
            field=models.CharField(default='Good', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='building_type',
            field=models.CharField(default='Detached', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='construction_type',
            field=models.CharField(default='Cement', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='deck',
            field=models.CharField(default='Y', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='fuel',
            field=models.CharField(default='Gas', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='garage_type',
            field=models.CharField(default='N/A', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='has_sewer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_dishwater',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_dryer',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_family_rooms',
            field=models.IntegerField(default=0, max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_garage_space',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_heating_zone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_refrigerator',
            field=models.IntegerField(default=1, max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_rooms',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='property',
            name='no_of_washer',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='property',
            name='type_of_floor',
            field=models.CharField(default='Wood Floors', max_length=200),
        ),
        migrations.AddField(
            model_name='property',
            name='water_source',
            field=models.CharField(default='Public Water', max_length=200),
        ),
    ]
