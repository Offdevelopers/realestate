# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-01 14:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(upload_to=b'')),
                ('bedroom', models.IntegerField()),
                ('bathroom', models.IntegerField()),
                ('full_address', models.TextField()),
                ('price', models.IntegerField()),
                ('area', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('year_built', models.DateField(null=True)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('developer_price', models.IntegerField()),
                ('agent_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Agent')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Developer')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Developer'),
        ),
    ]
