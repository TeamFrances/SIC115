# coding: utf-8

from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from setuptools.command.test import test

from main.forms import CuentaForm, ClienteForm, ProveedorForm, EquipoForm
from main.forms import EmpleadoForm
from main.forms import LoginForm
from main.forms import MovimientoForm
from main.forms import MovimientoFormMP
from main.forms import OrdenForm
from main.forms import ProductoForm
from main.forms import TransaccionForm
from main.models import MovimientoMp, EstadoFinalMP, Cliente, Proveedor, Inventario, Depreciacion, EquipoDespreciable, \
    CuentaMayor
from models import Cuenta, TipoCuenta, Transaccion, Empleado, Movimiento, ordenDeFabricacion, producto


@login_required(login_url='login')
def index_view(request):
    return render(request, 'main/index.html')


class ViewLoginForm(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('index')


def acerca_de_view(request):
    return render(request, 'main/acerca_de.html', {
        'titulo': 'Acerca de',
    })


def ayuda_view(request):
    return render(request, 'main/ayuda.html', {
        'titulo': 'Ayuda',
    })


def proveedores_list_view(request):
    return render(request, 'main/list_proveedores.html', {
        'titulo': 'Proveedores',
        'object_list': Proveedor.objects.all()
    })


def usuarios_list_view(request):
    return render(request, 'main/list_usuarios.html', {
        'titulo': 'Usuarios',
    })


def empleados_list_view(request):
    return render(request, 'main/list_empleados.html', {
        'titulo': 'Empleados',
    })


def cuentas_list_view(request):
    cuentas=CuentaForm()
    return render(request,  'main/cuentas_list.html',
     {'cuenta': cuentas,'titulo':'Cuentas',
     'activos':Cuenta.objects.filter(tipo=1),
     'pasivos':Cuenta.objects.filter(tipo=2),
     'patrimonios':Cuenta.objects.filter(tipo=3),
     'ResultadosD':Cuenta.objects.filter(tipo=4),
     'ResultadosH':Cuenta.objects.filter(tipo=5),
     'contraActivos':Cuenta.objects.filter(tipo=6)})


def cuenta_nueva(request):
    cuentas = CuentaForm()
    cuentaNueva = Cuenta()

    if request.method == 'POST':
        formulario = CuentaForm(request.POST)
        if formulario.is_valid():
            tipo=formulario.cleaned_data["tipo"]
            cuentaNueva.cuentaMayor=formulario.cleaned_data["cuenta_Mayor"]
            cuentaNueva.nombre = formulario.cleaned_data["nombre"]
            cuentaNueva.tipo = TipoCuenta.objects.get(id = int(tipo))

            cuentaNueva.rubro = formulario.cleaned_data["rubro"]
            rubro=cuentaNueva.rubro.numero
            cuentaNueva.codigo=str(cuentaNueva.cuentaMayor.codigo)+str(Cuenta.objects.filter(cuentaMayor=cuentaNueva.cuentaMayor).count()+1)
            cuentaNueva.saldoInicial=0
            cuentaNueva.debe=0
            cuentaNueva.haber=0
            cuentaNueva.saldoFinal=0

            cuentaNueva.save()
            return redirect('cuentas_list')
        else:
            return cuentas_list_view(request)

    return render(request,  'main/cuentas_list.html', {'cuenta': cuentas})


def ajustes_financieros_view(request):
    equipo=EquipoDespreciable.objects.all()
    return render(request, 'main/ajustes_financieros.html', {
        'titulo': 'Ajustes',
    })


def balance_general_view(request):
    return render(request, 'main/balance_general.html', {
        'titulo': 'Balance',
        'activos':Cuenta.objects.filter(tipo=1).order_by('-rubro').exclude(saldoFinal=0.0),
        'pasivos':Cuenta.objects.filter(tipo=2).order_by('-rubro').exclude(saldoFinal=0.0),
        'patrimonios':Cuenta.objects.filter(tipo=3).order_by('-rubro').exclude(saldoFinal=0.0)
    })


def estado_capital_view(request):
    return render(request, 'main/estado_capital.html', {
        'titulo': 'Estado de Capital','patrimonioDebe':Cuenta.objects.filter(acreedor=False,tipo=3),'patrimonioHaber':Cuenta.objects.filter(acreedor=True,tipo=3)
    })


def estado_resultados(request):
    return render(request, 'main/estado_resultados.html', {
        'titulo': 'Estado de Resultados','resultadoDebe':Cuenta.objects.filter(tipo_id=4),'resultadoHaber':Cuenta.objects.filter(tipo_id=5)
    })


def balance_comprobacion(request):
    return render(request, 'main/balance_comprobacion.html', {
        'titulo': 'Balance de Comprobación','cuentas': Cuenta.objects.all()
    })


def agregar_movimiento(request):

    formulario=TransaccionForm()

    if request.method == 'POST':
        futura = int(request.POST.get('mov'))
        movimientos = formset_factory(MovimientoForm, extra=futura)

        return render(request, 'main/libro_diario.html', {'titulo': 'Libro Diario', 'movimientos': movimientos, 'transaccion': formulario, 'agregar': True})
    elif request.method == 'GET':
        return render(request, 'main/libro_diario.html')


def getMovimientoForm(request):
    formulario = TransaccionForm()

    if request.method == "POST":
        mov = int(request.POST.get('mov'))
        movimientos = formset_factory(MovimientoForm, extra=mov)

        return render(request, 'main/form_libro_diario.html', {
            'movimientos': movimientos,
            'transaccion': formulario
        })


def agregar_Transaccion(request):
    transaccion=Transaccion()

    movimientoF = formset_factory(MovimientoForm)
    if request.method=='POST':
        formulario=TransaccionForm(request.POST)
        movimientos=movimientoF(request.POST)
        if formulario.is_valid() & movimientos.is_valid():
            empleado1=formulario.cleaned_data["empleado"]
            transaccion=Transaccion.objects.create(empleado=empleado1,monto=13,tipo=formulario.cleaned_data["tipo"],descripcion=formulario.cleaned_data["descripcion"],fecha=formulario.cleaned_data["fecha"])


            transaccion2=transaccion

            monto = testMovimientos(movimientos)

            if monto is not None:
                return guardarMovimientos(request,formulario,movimientos,transaccion2)
            else:
                return redirect('libro_diario')

    return redirect('libro_diario')



def libro_diario(request):
    transaccionF = TransaccionForm()

    return render(request, 'main/libro_diario.html', {
        'titulo': 'Libro Diario', 'transaccion': transaccionF, 'agregar': False,
          'transacciones': Movimiento.objects.all()

    })


def guardarMovimientos(request,formulario,movimientos,transaccion):
    for movimiento in movimientos :
        movimientoM=Movimiento()
        movimientoM.cuenta=movimiento.cleaned_data.get('cuenta')
        movimientoM.debe=movimiento.cleaned_data.get('tipo')
        movimientoM.cantidad=movimiento.cleaned_data.get('cantidad')

        Movimiento.objects.create(cuenta=movimiento.cleaned_data.get('cuenta') ,debe=movimiento.cleaned_data.get('tipo') ,cantidad=movimiento.cleaned_data.get('cantidad') ,transaccion=Transaccion.objects.get(id=Transaccion.objects.count()))
        cuentaModificar=Cuenta.objects.get(id=movimientoM.cuenta.id)

        cuentaModificar.save()
        if movimientoM.debe :
            cuentaModificar.debe=float(movimientoM.cantidad)+cuentaModificar.debe
            t=guardarCambioCuenta(cuentaModificar)
        else:
            cuentaModificar.haber=float(movimientoM.cantidad)+cuentaModificar.haber
            t=guardarCambioCuenta(cuentaModificar)

    return redirect('libro_diario')

def guardarCambioCuenta(cuenta_modificar):
    if cuenta_modificar.haber >= cuenta_modificar.debe:
        cuenta_modificar.saldoFinal = cuenta_modificar.haber - cuenta_modificar.debe
        cuenta_modificar.acreedor = True
    else:
        cuenta_modificar.saldoFinal = cuenta_modificar.debe - cuenta_modificar.haber
        cuenta_modificar.acreedor = False
    cuenta_modificar.save()
    return 1

def testMovimientos(movimientos):
    debe = 0
    haber = 0

    for movimiento in movimientos:
        if movimiento.is_valid():
            val = int(movimiento.cleaned_data.get("tipo"))
            if val :
                debe += float(movimiento.cleaned_data.get("cantidad"))
            else:
                haber += float(movimiento.cleaned_data.get("cantidad"))

    if haber != debe:
        return None
    else:
        return debe

def empleado_view(reques):
    if reques.method == 'POST':
        form = EmpleadoForm(reques.POST)
        if form.is_valid():
            form.save()
            return redirect('empleados_list')
    else:
        form = EmpleadoForm()

    return render(reques, 'main/agregarEmpleado.html', {'form': form, 'titulo': 'Agregar Empleado'})


class empleado_list(TemplateView):
    model = Empleado
    template_name = 'main/list_empleados.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/list_empleados.html', {
            'titulo': 'Empleados',
            'object_list': Empleado.objects.all()
        })


class Planilla(ListView):
    model = Empleado
    template_name = 'main/Planilla.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/Planilla.html', {
            'titulo':'Planilla',
            'object_list': Empleado.objects.all()
        })


class ListaOrdenes(ListView):
    model = ordenDeFabricacion
    template_name = 'main/ordenFabricacion.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/ordenFabricacion.html', {
            'titulo':'Ordenes de Fabricación',
            'object_list': ordenDeFabricacion.objects.all()
        })


class ListaProductos(ListView):
    model = producto
    template_name = 'main/produccion_ventas.html'

    def get(self, request, *args, **kwargs):
        # fecha = datetime.today().date()
        # fecha = fecha.replace(day=1)
        # productos = producto.objects.filter(ordenDeFabricacion__fechaExpedicion__year=fecha.year) \
        #     .filter(ordenDeFabricacion__fechaExpedicion__month=fecha.month)
        productos = producto.objects.all()

        totalMP = 0.0
        totalMOD = 0.0
        importe = 0.0
        costoArtTerminado = 0.0
        artTermDisp = 0.0
        costoVendido = 0.0

        for p in productos:
            totalMP += p.ordenDeFabricacion.totalMP()

        for p in productos:
            totalMOD += p.ordenDeFabricacion.totalMOD()

        for p in productos:
            importe += p.ordenDeFabricacion.importe()

        for p in productos:
            costoArtTerminado += p.costoArtTerminado()

        for p in productos:
            artTermDisp += p.artTerDisp()

        for p in productos:
            costoVendido += p.costoVendido()

        # if len(args) > 0:
        #     fecha.replace(month=args.index('mes'))
        #     fecha.replace(args.index('año'))

        return render(request, self.template_name, {
            'titulo': 'Producción y Ventas',
            'object_list': productos,
            'totalMP': totalMP,
            'totalMOD': totalMOD,
            'importe': importe,
            'costoArtTerminado': costoArtTerminado,
            'artTermDisp': artTermDisp,
            'costoVendido': costoVendido
        })

def equipo_view(request):
    equipoForm=EquipoForm()

    return render(request ,'main/equipo_list.html',{'titulo':'Compra','comprarF':equipoForm})

class listaMovimientosMP(ListView):
    model = MovimientoMp
    template_name = 'main/inventarioMP.html'

    def get(self, request, *args, **kwargs):
        movimientos = MovimientoMp.objects.all()
        total_anterior = EstadoFinalMP.objects.last()
        res = []

        if total_anterior is not None:
            m = {}
            for movimiento in movimientos:
                if movimiento.tipo == 'E':
                    if len(res) == 0:
                        m["cantidad"] = total_anterior.cantidad + movimiento.idMov
                        m["precioUnitario"] = total_anterior.precioUnitario + movimiento.idMov
                        m["total"] = total_anterior .getTotal() + movimiento.idMov
                    else:
                        m["cantidad"] = movimientos + movimiento.idMov
                        m["precioUnitario"] = total_anterior.precioUnitario + movimiento.idMov
                        m["total"] = total_anterior .getTotal() + movimiento.idMov


        return render(request, 'main/inventarioMP.html', {
            'titulo':'Inventario de materia Prima',
            'object_list': MovimientoMp.objects.all(),
            'col_resultados': res
        })


class CrearOrde(CreateView):
    model = ordenDeFabricacion
    form_class = OrdenForm
    template_name = 'main/agregarOrden.html'
    success_url = reverse_lazy('ordenes')


class crearMovimientoMP(CreateView):
    model = MovimientoMp
    form_class = MovimientoFormMP
    template_name = 'main/agregarMovimientoMP.html'
    success_url = reverse_lazy('inventario')


class crearProducto(CreateView):
    model = producto
    form_class = ProductoForm
    template_name = 'main/agregarProducto.html'
    success_url = reverse_lazy('produccion')


class crearCuenta(CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = 'main/agregarCuenta.html'
    success_url = reverse_lazy('cuentas_list')


class listClientes(ListView):
    model = Cliente
    template_name = 'main/listaClientes.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/listaClientes.html', {
            'titulo':'Clientes',
            'object_list': Cliente.objects.all()
        })


class Empleado_DetailView(DetailView):
    model = Empleado
    template_name = 'main/empleado_details.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {
    #         'empleado': self.model.objects.filter(id=kwargs['pk'])
    #     })


class listaProveedores(ListView):
    model = Proveedor
    template_name = 'main/list_proveedores.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/list_proveedores.html', {
            'titulo':'Proveedores',
            'object_list': Proveedor.objects.all()
        })

class crearClente(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'main/crearCliente.html'
    success_url = reverse_lazy('clientes')


class crearProveedor(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'main/crearProveedor.html'
    success_url = reverse_lazy('proveedores_list')


class listaMaq(ListView):
    model = Inventario
    template_name = 'main/maquinaria-equipo.html'

    def get(self, request, *args, **kwargs):
         return render(request, 'main/maquinaria-equipo.html', {
        'titulo':'Maquinaria, Mobiliario y Equipo',
        'object_list': Inventario.objects.all()
        })


def compraEquipo(request):

    if request.method=='POST':
        equipo=EquipoForm(request.POST)
        if equipo.is_valid():
            nombre=equipo.cleaned_data['nombre']
            vida=equipo.cleaned_data['vida_util']
            compra=equipo.cleaned_data['valor_de_compra']
            recuperacion=equipo.cleaned_data['recuperacion']

            deprecio=(compra-recuperacion)/vida
            Cuenta.objects.create(nombre="depreciacion "+nombre,tipo=TipoCuenta.objects.get(id=1),debe=0,haber=0,saldoFinal=0,codigo="127"+str(CuentaMayor.objects.filter(id=14).count()+1))
            Depreciacion.objects.create(cantidad=deprecio,cuentaLibro=Cuenta.objects.get(id=Cuenta.objects.count()))
            Cuenta.objects.create(nombre=nombre,tipo=TipoCuenta.objects.get(id=1),debe=compra,haber=0,saldoFinal=compra,codigo="123"+str(CuentaMayor.objects.filter(id=9).count()+1))
            EquipoDespreciable.objects.create(nombre=nombre,vidaUtil=vida,valorRecuperacion=recuperacion,cuentaValorCompra=Cuenta.objects.get(id=Cuenta.objects.count()),depreciacion=Depreciacion.objects.get(id=Depreciacion.objects.count()),valorActual=compra)

            return reverse('ajustes_financieros')


