# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-01 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0007_auto_20170330_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='profile',
            field=models.ImageField(blank=True, default='static/profiles/default.png', upload_to='static/profiles/'),
        ),
    ]