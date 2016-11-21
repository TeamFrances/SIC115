"""frances URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="administracion"),
    url(r'^$', views.index_view, name="index"),
    url(r'^login$', views.ViewLoginForm.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^acerca_de/', views.acerca_de_view, name="acerca_de"),
    url(r'^ayuda/', views.ayuda_view, name="ayuda"),
    url(r'^proveedores/', views.proveedores_list_view, name="proveedores_list"),
    url(r'^usuarios/', views.usuarios_list_view, name="usuarios_list"),

    url(r'^cuentas/', views.cuentas_list_view, name="cuentas_list"),
    url(r'^nuevaCuenta/',views.cuenta_nueva,name='cuenta_nueva'),
    url(r'^agregar_Movimiento/',views.agregar_movimiento,name='agregar_movimiento'),
    url(r'^agregar_Transaccion/',views.agregar_Transaccion,name='transaccion_nueva'),
    url(r'^ajustes_financieros/', views.ajustes_financieros_view, name="ajustes_financieros"),
    url(r'^balance/', views.balance_general_view, name="balance_general"),
    url(r'^estado_capital/', views.estado_capital_view, name="estado_capital"),
    url(r'^estado_resultados/', views.estado_resultados, name="estado_resultados"),
    url(r'^balance_comprobacion/', views.balance_comprobacion, name="balance_comprobacion"),
    url(r'^libro_diario/', views.libro_diario, name="libro_diario"),

    url(r'^agregar_empleado/', views.empleado_view, name="agregar_empleado"),
    url(r'^planilla/', views.planilla.as_view(), name="planilla"),
    url(r'^empleados/', views.empleado_list.as_view(), name="empleados_list"),

    url(r'^ordenes/', views.listaOrdenes.as_view(), name="ordenes"),
    url(r'^crearOrde/', views.CrearOrde.as_view(), name="crearOrden"),

    url(r'^produccion/', views.listaProductos.as_view(), name="produccion"),
    url(r'^inventario/', views.listaMovimientosMP.as_view(), name="inventario"),



]
