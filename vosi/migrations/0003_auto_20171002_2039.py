# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-02 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vosi', '0002_voresource_capability_appname'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='appname',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='availabilityoption',
            name='appname',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]