# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-30 23:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activelife', '0009_auto_20160331_0120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activlcritmetierromeap',
            old_name='tiers',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='activlcritmetierromedp',
            old_name='tiers',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='activlcritmetierromefi',
            old_name='tiers',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='activlcritmetierromegd',
            old_name='tiers',
            new_name='parent',
        ),
    ]