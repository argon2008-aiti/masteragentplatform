# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-03 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_daypurchase_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='daypurchase',
            name='month',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
