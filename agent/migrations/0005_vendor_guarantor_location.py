# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-27 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0004_vendor_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='guarantor_location',
            field=models.CharField(default='Accra', max_length=100),
        ),
    ]
