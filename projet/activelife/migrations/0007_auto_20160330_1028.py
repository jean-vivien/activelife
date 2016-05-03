# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-30 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activelife', '0006_romedp_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='romeap',
            old_name='code',
            new_name='codeOGR',
        ),
        migrations.AddField(
            model_name='romeap',
            name='codeROME',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='romeap',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='activelife.ROMEFi'),
        ),
        migrations.AddField(
            model_name='romefi',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='activelife.ROMEDP'),
        ),
    ]