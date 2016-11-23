# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-21 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoMp',
            fields=[
                ('idMov', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('E', 'Entrada'), ('S', 'Salida')], max_length=1)),
                ('fecha', models.DateField()),
                ('nombre', models.CharField(max_length=50)),
                ('cantidad', models.FloatField(default=0.0)),
                ('precioUnitario', models.FloatField(default=0.0)),
            ],
        ),
    ]