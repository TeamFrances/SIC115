# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-14 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20161113_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='rubro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Rubro'),
        ),
    ]