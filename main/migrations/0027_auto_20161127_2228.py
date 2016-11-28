# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-28 04:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_empleado_eficiencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientomp',
            name='proveedor',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Proveedor'),
        ),
        migrations.AddField(
            model_name='ordendefabricacion',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Cliente'),
        ),
    ]