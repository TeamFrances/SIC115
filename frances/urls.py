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
from wkhtmltopdf.views import PDFTemplateView

from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="administracion"),
    url(r'^$', views.index_view, name="index"),
    url(r'^login$', views.ViewLoginForm.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^acerca_de/$', views.acerca_de_view, name="acerca_de"),
    url(r'^ayuda/$', views.ayuda_view, name="ayuda"),
    url(r'^proveedores/$', views.proveedores_list_view, name="proveedores_list"),
    url(r'^usuarios/$', views.usuarios_list_view, name="usuarios_list"),

    url(r'^cuentas/$', views.cuentas_list_view, name="cuentas_list"),
    url(r'^add_cuenta/$', views.crearCuenta.as_view(), name="add_cuenta"),

    url(r'^nuevaCuenta/$',views.cuenta_nueva,name='cuenta_nueva'),
    url(r'^agregar_Movimiento/$',views.agregar_movimiento,name='agregar_movimiento'),
    url(r'^get_movimiento_form/$',views.getMovimientoForm,name='get_movimiento_form'),
    url(r'^agregar_Transaccion/$',views.agregar_Transaccion,name='transaccion_nueva'),
    url(r'^ajustes_financieros/$', views.ajustes_financieros_view, name="ajustes_financieros"),
    url(r'^balance/$', views.balance_general_view, name="balance_general"),
    url(r'^estado_capital/$', views.estado_capital_view, name="estado_capital"),
    url(r'^estado_resultados/$', views.estado_resultados, name="estado_resultados"),
    url(r'^balance_comprobacion/$', views.balance_comprobacion, name="balance_comprobacion"),

    url(r'^libro_diario/$', views.libro_diario, name="libro_diario"),

    url(r'^agregar_empleado/$', views.empleado_view, name="agregar_empleado"),
    url(r'^planilla/$', views.Planilla.as_view(), name="planilla"),

    url(r'^empleados/$', views.empleado_list.as_view(), name="empleados_list"),
    url(r'^empleado/(?P<pk>[\w]+)$', views.Empleado_DetailView.as_view(), name="empleado_detail"),

    url(r'^ordenes/$', views.ListaOrdenes.as_view(), name="ordenes"),
    url(r'^crearOrde/$', views.CrearOrde.as_view(), name="crearOrden"),

    url(r'^produccion/$', views.ListaProductos.as_view(), name="produccion"),
    url(r'^add_producto/$', views.crearProducto.as_view(), name="add_producto"),

    url(r'^inventario/$', views.listaMovimientosMP.as_view(), name="inventario"),
    url(r'^add_mov/$', views.crearMovimientoMP.as_view(), name="add_mov"),
    url(r'^clientes/', views.listClientes.as_view(), name="clientes"),
    url(r'^agregarCliente/', views.crearClente.as_view(), name="agregarCliente"),

    url(r'^pdf/balance_comprobacion$', PDFTemplateView.as_view(template_name='main/balance_comprobacion.html', filename='balance_comprobacion.pdf'), name="pdf"),
    url(r'^pdf/estado_resultados$', PDFTemplateView.as_view(template_name='main/estado_resultados.html', filename='estado_resultados.pdf'), name="pdf"),
    url(r'^pdf/estado_capital$', PDFTemplateView.as_view(template_name='main/estado_capital.html', filename='estado_capital.pdf'), name="pdf"),
    url(r'^pdf/balance_general$', PDFTemplateView.as_view(template_name='main/balance_general.html', filename='balance_general.pdf'), name="pdf"),

    url(r'^agregarProveedor/', views.crearProveedor.as_view(), name="agregarProveedor"),

    url(r'^maquinaria/', views.listaMaq.as_view(), name="maquinaria"),
    url(r'^compra_equipo/', views.compraEquipo, name="compra_equipo")




]
