# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-25 23:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20170407_2216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendorbooking',
            options={'ordering': ['-date']},
        ),
    ]
