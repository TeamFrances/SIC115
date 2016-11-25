from django.contrib import admin

from main.models import MovimientoMp
from models import Cuenta,TipoCuenta,Rubro, Transaccion,TipoTransaccion,Empleado,Puesto,Movimiento,Configuracion, ordenDeFabricacion, producto

# Register your models here.
admin.site.register(Cuenta)
admin.site.register(TipoCuenta)
admin.site.register(Rubro)
admin.site.register(Transaccion)
admin.site.register(TipoTransaccion)
admin.site.register(Empleado)
admin.site.register(Puesto)
admin.site.register(Movimiento)
admin.site.register(Configuracion)
admin.site.register(ordenDeFabricacion)
admin.site.register(producto)
admin.site.register(MovimientoMp)



