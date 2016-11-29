# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime, time, timedelta, date

from django.core.urlresolvers import reverse
from django.db import models


class Puesto(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    salarioMensual = models.FloatField(default=0.0, null=False)

    def __str__(self):
        return self.nombre

    def get_salario_diario(self):
        return self.salarioMensual / 30

    def get_salario_real(self):
        return (self.get_salario_diario()*7)/5.5

    def get_salario_nominal(self):
        return self.get_salario_real()*7

    def get_vacaciones(self):
        return self.get_salario_diario()*15*1.3

    def get_prestaciones(self):
        return (self.get_salario_diario() * 15) * 0.1525

    def get_cotizaciones_y_vacaciones(self):    #El dato 0.1525 debe sacarse de la BD, y es el total de prestaciones
        return self.get_vacaciones() + self.get_prestaciones()

    def get_provision_semanal(self):
        return self.get_cotizaciones_y_vacaciones() / 52

    def get_cotizacion_semanal(self):
        return self.get_salario_nominal()*0.1525



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
    eficiencia = models.FloatField(default=0.9)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
    activo = models.BooleanField()
    fecha_contratacion = models.DateField(default='2001-01-01')

    def __str__(self):
        return self.nombres+" "+self.apellidos

    def get_dias_contratado(self):
        f1 = self.fecha_contratacion
        delta = date.today() - f1

        return delta.days

    def get_aguinaldo(self):
        dias = self.get_dias_contratado()
        salario_diario = self.puesto.get_salario_diario()

        if dias >= 0 and dias < 1080:           #Si ha trabajado hasta menos de 3 años
            # if datetime.today() >= date.today().replace(month=12, day=12):      #Si hoy
            return salario_diario*15
        elif dias >= 1080 and dias < 3600:      #Si ha trabajado desde 3 hasta 10 años
            return salario_diario*19
        elif dias >= 3600:                      #Si ha trabajado de 10 años en adelante
            return salario_diario*21

    def get_aguinaldo_semanal(self):
        return self.get_aguinaldo()/52

    def get_salario_semanal(self):
        sum = self.puesto.get_salario_nominal() + self.get_aguinaldo_semanal() + \
              self.puesto.get_provision_semanal() + self.puesto.get_cotizacion_semanal()

        return sum

    def get_factor_recargo(self):
        return self.get_salario_semanal() / self.puesto.get_salario_nominal()

    def get_factor_recargo_eficiencia(self):
        return self.get_factor_recargo() / self.eficiencia

    def get_salario_mensual(self):
        return self.get_salario_semanal() * 4

    def get_absolute_url(self):
        return reverse('empleado_detail', kwargs={"pk":self.pk})


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

    def __str__(self):
        return self.marca


class TipoTransaccion(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=49, null=False)

    def __str__(self):
        return self.nombre


class Rubro(models.Model):
    id = models.IntegerField(editable=False,auto_created=True, primary_key=True)
    numero=models.IntegerField()
    nombre=models.CharField(max_length=21, null=False)

    def __unicode__(self):
        return self.nombre


class TipoCuenta(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    codigo=models.CharField(max_length=5, null=False, default='111')
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre+"  "+self.codigo


class CuentaMayor(models.Model):
    id=models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre=models.CharField(max_length=50, null=False)
    codigo=models.CharField(max_length=5, null=False)
    def __str__(self):
        return self.nombre



class Cuenta(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    saldoInicial = models.FloatField(default=0.0)
    nombre=models.CharField(max_length=50,  null=False, unique=True)
    tipo=models.ForeignKey(TipoCuenta, null=False)
    debe = models.FloatField(default=0.0)
    haber = models.FloatField(default=0.0)
    saldoFinal = models.FloatField(default=0.0)
    codigo= models.CharField(max_length=5, null=False, default=1)
    acreedor=models.BooleanField(default=True)
    rubro=models.ForeignKey(Rubro, null=False)
    cuentaMayor=models.ForeignKey(CuentaMayor,null=True)

    def codigo2(self):

        if self.id <=9:
            cod=str(self.tipo.id)+str(self.rubro.numero)+"0"+str(+self.id)
        else:
            cod=str(self.tipo.id)+str(self.rubro.numero)+str(self.id)
        return cod

    def __str__(self):
        return self.nombre

    def saldoF(self):
        return self.haber-self.debe


class Cliente(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=9, null=False)

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    id = models.IntegerField(editable=False, auto_created=True, primary_key=True)
    descripcion = models.TextField(max_length=100, null=False)
    valor = models.FloatField(default=0.0)

    def __str__(self):
        return self.descripcion


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


class Configuracion(models.Model):
    id=models.IntegerField(editable=False, auto_created=True, primary_key=True)
    nombre=models.CharField(max_length=100, null=False, blank=False)
    valor=models.FloatField(null=False,blank=False)

    def __str__(self):
        return self.nombre


class ordenDeFabricacion(models.Model):
    numOrden=models.IntegerField(editable=False, auto_created=True, primary_key=True, unique=True)
    cliente=models.ForeignKey(Cliente, default=1)
    fechaExpedicion=models.DateField()
    fechaRequerida=models.DateField()
    materal=models.CharField(max_length=100, null=False)
    catidadMP=models.FloatField()
    costoUnitarioMP=models.FloatField()
    obrero=models.ForeignKey(Empleado, null=False)
    numHoras=models.IntegerField()
    costoHora=models.FloatField()
    tasaCIF=models.FloatField()


    def totalMP(self):
        return self.catidadMP*self.costoUnitarioMP

    def totalMOD(self):
        return self.numHoras*self.costoHora

    def importe(self):
        return (self.catidadMP*self.costoUnitarioMP)*self.tasaCIF

    def __str__(self):
        numeroOrden=str(self.numOrden)
        return numeroOrden+" "+self.materal



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
    nuneroArticulos=models.IntegerField()



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
    proveedor=models.ForeignKey(Proveedor, blank=True, default=1)
    tipo = models.CharField(max_length=1, choices=tipo_opt, null=False)
    fecha=models.DateField()
    nombre=models.CharField(max_length=50)
    cantidad=models.FloatField()
    precioUnitario= models.FloatField()

    def getTotalMovimiento(self):
        return self.cantidad*self.precioUnitario

    def __str__(self):
        return str(self.nombre)


class EstadoFinalMP(models.Model):
    idMov = models.IntegerField(auto_created=True, primary_key=True)
    fechaFin = models.DateField()
    cantidad = models.IntegerField(null=False, blank=False)
    precioUnitario = models.FloatField(null=False, blank=False)

    def __unicode__(self):
        return "Cierre al " + str(self.fechaFin.day) + "/" + str(self.fechaFin.month) + "/" + str(self.fechaFin.year)

    def getTotal(self):
        return self.cantidad * self.precioUnitario

class Depreciacion(models.Model):
    id=models.IntegerField(editable=False, auto_created=True,primary_key=True)
    cantidad=models.FloatField(max_length=50)
    cuentaLibro=models.ForeignKey(Cuenta,null=False)


class EquipoDespreciable(models.Model):
    id=models.IntegerField(editable=False, auto_created=True,primary_key=True)
    nombre=models.CharField(max_length=50)
    vidaUtil=models.IntegerField()
    valorRecuperacion=models.FloatField(default=0.0)
    cuentaValorCompra=models.ForeignKey(Cuenta,null=False)
    depreciacion=models.ForeignKey(Depreciacion,null=False)
    valorActual=models.FloatField(default=0.0,null=True)
    def __str__(self):
        return self.nombre