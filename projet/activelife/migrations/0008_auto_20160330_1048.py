# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-30 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activelife', '0007_auto_20160330_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='romeap',
            name='codeROME',
            field=models.CharField(default='?0000', max_length=5),
        ),
    ]
