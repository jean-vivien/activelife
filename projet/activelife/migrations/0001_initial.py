# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-21 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ACTIVLCandidat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('Femme', 'Femme'), ('Homme', 'Homme'), ('Non renseign\xe9', 'Non renseign\xe9')], max_length=100)),
                ('anniversaire', models.DateTimeField(verbose_name='Date de naissance')),
                ('identPE', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLCritere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib', models.CharField(max_length=100)),
                ('typCrit', models.CharField(choices=[('Discret', 'Discret'), ('Continu', 'Continu')], max_length=100)),
                ('unite', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLCritGeo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib', models.CharField(default='Geographie', editable=False, max_length=100)),
                ('valeur', models.CharField(choices=[('Mer', 'Mer'), ('Montagne', 'Montagne'), ('Campagne', 'Campagne')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLCritIdees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib', models.CharField(default='Orientation politique', editable=False, max_length=100)),
                ('valeur', models.CharField(choices=[('Verts', 'Verts'), ('FrontDeGauche', 'FrontDeGauche'), ('PS', 'PS'), ('UDI', 'UDI'), ('LR', 'LR'), ('FN', 'FN')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLCritPrixM2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib', models.CharField(default="Prix du m2 \xe0 l'achat", editable=False, max_length=100)),
                ('valeur', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLCritVillePop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib', models.CharField(default='Population urbaine', editable=False, max_length=100)),
                ('valeur', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLLienTiersValeurCritere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiersCandidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCandidat')),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLRecruteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raisonSociale', models.CharField(max_length=200)),
                ('SIRET', models.CharField(max_length=14)),
                ('valCritereGeo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritGeo')),
                ('valCritereIdees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritIdees')),
                ('valCriterePrixM2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritPrixM2')),
                ('valCritereVillePop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritVillePop')),
            ],
        ),
        migrations.CreateModel(
            name='ACTIVLValeurCritere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.CharField(max_length=100)),
                ('critere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritere')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='ROMEAp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ROMEDP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ROMEFi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ROMEGD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.Question'),
        ),
        migrations.AddField(
            model_name='activllientiersvaleurcritere',
            name='tiersRecruteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLRecruteur'),
        ),
        migrations.AddField(
            model_name='activllientiersvaleurcritere',
            name='valeur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLValeurCritere'),
        ),
        migrations.AddField(
            model_name='activlcandidat',
            name='valCritereGeo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritGeo'),
        ),
        migrations.AddField(
            model_name='activlcandidat',
            name='valCritereIdees',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritIdees'),
        ),
        migrations.AddField(
            model_name='activlcandidat',
            name='valCriterePrixM2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritPrixM2'),
        ),
        migrations.AddField(
            model_name='activlcandidat',
            name='valCritereVillePop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activelife.ACTIVLCritVillePop'),
        ),
    ]
