# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20160619_1200'),
    ]
    operations = [
        migrations.AddField(
            model_name='posts',
            name='return_date',
            field=models.DateField(null=True),
        ),
    ]
