# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-21 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_movimientomp'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendefabricacion',
            name='fechaExpedicion',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='ordendefabricacion',
            name='fechaRequerida',
            field=models.DateField(default='2000-01-01'),
        ),
    ]