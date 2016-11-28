from django.contrib import admin

from main.models import MovimientoMp, Inventario, Proveedor, Cliente
from models import Cuenta,TipoCuenta,Rubro, Transaccion,TipoTransaccion,Empleado,Puesto,Movimiento,Configuracion, ordenDeFabricacion, producto

# Register your models here.

class cuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre','id',  'codigo2', 'rubro', 'tipo')
    list_filter = ('tipo', 'rubro')
    search_fields = ('nombre', 'codigo', 'rubro','tipo')

class empleadoAdmin(admin.ModelAdmin):
    list_display = ('nombres','id', 'apellidos', 'edad', 'sexo', 'direccion', 'telefono', 'contacto','dui', 'nit', 'afp', 'puesto', 'activo')
    list_filter = ('edad','sexo','puesto', 'activo')
    search_fields = ('id','nombres', 'apellidos', 'edad', 'sexo', 'direccion', 'telefono', 'contacto','dui', 'nit', 'afp', 'puesto',)

class movAdmin(admin.ModelAdmin):
    list_display = ('proveedor','nombre','idMov', 'fecha', 'cantidad', 'tipo', 'precioUnitario')
    list_filter = ('tipo','fecha')
    search_fields = ('idMov','nombre', 'fecha', 'cantidad', 'tipo', 'precioUnitario')

class productoAdmin(admin.ModelAdmin):
    list_display = ('nombre','numProducto', 'ordenDeFabricacion', 'nuneroArticulos','costoUnitario')
    search_fields = ('numProducto','nombre', 'ordenDeFabricacion', 'nuneroArticulos','costoUnitario')

class ordenAdmin(admin.ModelAdmin):
    list_display = ('cliente','numOrden','fechaExpedicion', 'fechaRequerida', 'materal','catidadMP','costoUnitarioMP','totalMP','obrero','numHoras',
                    'costoHora','totalMOD','tasaCIF', 'importe')
    search_fields = ('numOrden','fechaExpedicion', 'fechaRequerida', 'materal','catidadMP','costoUnitarioMP','totalMP','obrero','numHoras',
                     'costoHora','totalMOD','tasaCIF', 'importe')

class movimientoAdmin(admin.ModelAdmin):
    list_display = ('transaccion','id', 'cuenta', 'debe', 'cantidad')
    search_fields = ('id','transaccion', 'cuenta', 'cantidad')

class transaccionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'id', 'fecha', 'empleado', 'tipo', 'monto')
    list_filter = ('tipo', 'empleado')
    search_fields = ('id', 'fecha', 'empleado', 'tipo', 'descripcion', 'monto')


class puestoAdmin(admin.ModelAdmin):
    list_display = ('nombre','id',  'salarioMensual')
    search_fields = ('id', 'nombre', 'salarioMensual')

class tipoCuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id', 'codigo')
    search_fields = ('id', 'nombre', 'codigo')


class rubroAdmin(admin.ModelAdmin):
    list_display = ( 'nombre','numero','id')
    search_fields = ('id', 'numero', 'nombre')

class inventarioAdmin(admin.ModelAdmin):
    list_display = ('descripcion','id',  'valor')
    search_fields = ('id', 'descripcion', 'valor')

class clienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id', 'telefono')
    search_fields = ('nombre', 'id','telefono')


class proveedorteAdmin(admin.ModelAdmin):
    list_display = ('marca','id', 'direccion', 'telefono', 'nit')
    search_fields = ('marca','id', 'direccion', 'telefono', 'nit')

admin.site.register(Cuenta, cuentaAdmin)
admin.site.register(TipoCuenta, tipoCuentaAdmin)
admin.site.register(Rubro, rubroAdmin)
admin.site.register(Transaccion, transaccionAdmin)
admin.site.register(TipoTransaccion)
admin.site.register(Empleado, empleadoAdmin)
admin.site.register(Puesto, puestoAdmin)
admin.site.register(Movimiento, movimientoAdmin)
admin.site.register(Configuracion)
admin.site.register(ordenDeFabricacion, ordenAdmin)
admin.site.register(producto, productoAdmin)
admin.site.register(MovimientoMp, movAdmin)
admin.site.register(Inventario, inventarioAdmin)
admin.site.register(Proveedor, proveedorteAdmin)
admin.site.register(Cliente, clienteAdmin)


