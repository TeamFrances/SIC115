# coding: utf-8
from __future__ import unicode_literals

from django.db import models


class Puesto(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    salarioNominalDiario = models.FloatField(default=0.0, null=False)

    def __str__(self):
        return self.nombre


# Create your models here.
class Empleado(models.Model):
    sexo_opt = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )

    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombres = models.CharField(max_length=50, null=False)
    apellidos = models.CharField(max_length=50, null=False)
    edad = models.IntegerField(null=False)
    sexo = models.CharField(max_length=1, choices=sexo_opt, null=False)
    direccion = models.TextField(max_length=200, null=False)
    telefono = models.CharField(max_length=9, null=False)
    contacto = models.CharField(max_length=9, null=False)
    dui = models.CharField(max_length=10, null=False)
    nit = models.CharField(max_length=17, null=False)
    afp = models.CharField(max_length=12, null=False)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombres+" "+self.apellidos

    def salReal(self):
        return (self.puesto.salarioNominalDiario*7)/5.5


class Usuario(models.Model):
    id = models.TextField(max_length=25, primary_key=True, auto_created=False, editable=True)
    password = models.CharField(max_length=64, null=False)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)


class Proveedor(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    marca = models.CharField(max_length=50, null=False)
    direccion = models.TextField(max_length=200, null=False)
    telefono = models.CharField(max_length=9, null=False)
    nit = models.CharField(max_length=17, null=False)


class TipoTransaccion(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=49, null=False)

    def __str__(self):
        return self.nombre


class Rubro(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    numero=models.IntegerField()
    nombre=models.CharField(max_length=21, null=False)

    def __unicode__(self):
        return self.nombre


class TipoCuenta(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    codigo=models.CharField(max_length=5, null=False, default='111')
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    saldoInicial = models.FloatField(default=0.0)
    nombre=models.CharField(max_length=50,  null=False)
    tipo=models.ForeignKey(TipoCuenta, null=False)
    debe = models.FloatField(default=0.0)
    haber = models.FloatField(default=0.0)
    saldoFinal = models.FloatField(0.0)
    codigo= models.CharField(max_length=5, null=False, default=1)
    acreedor=models.BooleanField(default=True)
    rubro=models.ForeignKey(Rubro, null=False)

    def __str__(self):
        return self.nombre

    def saldoF(self):
        return self.haber-self.debe


class Cliente(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=9, null=False)


class Inventario(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    descripcion = models.TextField(max_length=100, null=False)
    valor = models.FloatField(default=0.0)


class Transaccion(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    fecha = models.DateField()
    empleado = models.ForeignKey(Empleado, null=False)
    tipo = models.ForeignKey(TipoTransaccion, null=False)
    descripcion=models.TextField(max_length=10, null=True)
    monto = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.id)


class Movimiento(models.Model):
    id=models.IntegerField(editable=False, auto_created=True,primary_key=True)
    transaccion=models.ForeignKey(Transaccion, null=False)
    cuenta=models.ForeignKey(Cuenta, null=False)
    debe=models.BooleanField()
    cantidad=models.FloatField(default=0.0, null=True)

    def __str__(self):
        return str(self.cantidad)


class Prestacion(models.Model):
    id=models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre=models.CharField(max_length=100, null=False)
    porcentage= models.FloatField(default=0.0)

    def __str__(self):
        return self.nombre


class ordenDeFabricacion(models.Model):
    numOrden=models.IntegerField(editable=False, auto_created=True, primary_key=True, unique=True)
    fechaExpedicion=models.DateField(default='2000-01-01')  #Fecha en que la orden se generó
    fechaRequerida=models.DateField(default='2000-01-01')   #Fecha en que la orden se entregó y se descargó de inventario
    materal=models.CharField(max_length=100, null=False)
    catidadMP=models.FloatField(default=0.0)
    costoUnitarioMP=models.FloatField(default=0.0)
    obrero=models.ForeignKey(Empleado, null=False)
    numHoras=models.IntegerField()
    costoHora=models.FloatField(default=0.0)
    tasaCIF=models.FloatField(default=0.0)

    def totalMP(self):
        return self.catidadMP*self.costoUnitarioMP

    def totalMOD(self):
        return self.numHoras*self.costoHora

    def importe(self):
        return (self.catidadMP*self.costoUnitarioMP)*self.tasaCIF

    def __str__(self):
        numeroOrden=str(self.numOrden)
        return numeroOrden

class producto(models.Model):
    numProducto=models.IntegerField(editable=False, auto_created=True, primary_key=True, unique=True)
    nombre=models.CharField(max_length=50, null=False)
    ordenDeFabricacion=models.ForeignKey(ordenDeFabricacion, null=False)
    inventarioInicialMp=models.FloatField(default=0.0)
    compras=models.FloatField(default=0.0)
    inventarioFinal=models.FloatField(default=0.0)
    invIniPenP=models.FloatField(default=0.0)
    invFinalPenP=models.FloatField(default=0.0)
    invInicialProductTerminado=models.FloatField(default=0.0)
    invFinalProductTerminado=models.FloatField(default=0.0)
    nuneroArticulos=models.IntegerField(default=0.0)



    def MPDisp(self):
        return self.inventarioInicialMp+self.compras

    def MPUtilizada(self):
        return self.ordenDeFabricacion.totalMP()

    def costoArtTerminado(self):
        return self.ordenDeFabricacion.totalMP()+self.invIniPenP+self.ordenDeFabricacion.totalMOD()+self.ordenDeFabricacion.importe()-self.invFinalPenP

    def artTerDisp(self):
        return self.ordenDeFabricacion.totalMP()+self.invIniPenP+self.ordenDeFabricacion.totalMOD()+self.ordenDeFabricacion.importe()-self.invFinalPenP+self.invInicialProductTerminado

    def costoVendido(self):
        return self.ordenDeFabricacion.totalMP()+self.invIniPenP+self.ordenDeFabricacion.totalMOD()+self.ordenDeFabricacion.importe()-self.invFinalPenP+self.invInicialProductTerminado-self.invFinalProductTerminado

    def costoUnitario(self):
        return (self.ordenDeFabricacion.totalMP()+self.invIniPenP+self.ordenDeFabricacion.totalMOD()+self.ordenDeFabricacion.importe()-self.invFinalPenP+self.invInicialProductTerminado-self.invFinalProductTerminado)/self.nuneroArticulos

    def __str__(self):
        return self.nombre


class MovimientoMp(models.Model):
    tipo_opt = (
        ('E', 'Entrada'),
        ('S', 'Salida'),
    )
    idMov=models.IntegerField(primary_key=True, editable=False, auto_created=True)
    tipo = models.CharField(max_length=1, choices=tipo_opt, null=False)
    fecha=models.DateField()
    nombre=models.CharField(max_length=50)
    cantidad=models.FloatField(default=0.0)
    precioUnitario= models.FloatField(default=0.0)

    def totalMovimiento(self):
        return self.cantidad*self.precioUnitario



