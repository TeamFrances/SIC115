# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-11-19 23:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_ordendefabricacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='producto',
            fields=[
                ('numProducto', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('inventarioInicialMp', models.FloatField(default=0.0)),
                ('compras', models.FloatField(default=0.0)),
                ('inventarioFinal', models.FloatField(default=0.0)),
                ('invIniPenP', models.FloatField(default=0.0)),
                ('invFinalPenP', models.FloatField(default=0.0)),
                ('invInicialProductTerminado', models.FloatField(default=0.0)),
                ('invFinalProductTerminado', models.FloatField(default=0.0)),
                ('nuneroArticulos', models.IntegerField(default=0.0)),
                ('ordenDeFabricacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ordenDeFabricacion')),
            ],
        ),
    ]