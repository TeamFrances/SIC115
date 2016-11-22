# coding: utf-8
import calendar

from datetime import date, datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.dates import timezone_today
from django.views.generic.edit import FormView, CreateView

from main.forms import CuentaForm
from main.forms import EmpleadoForm
from main.forms import LoginForm
from main.forms import MovimientoForm
from main.forms import TransaccionForm,OrdenForm
from main.models import MovimientoMp
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
                   'activos': Cuenta.objects.filter(tipo=1),
                   'pasivos': Cuenta.objects.filter(tipo=2),
                   'patrimonios': Cuenta.objects.filter(tipo=3),
                   'resultadosA': Cuenta.objects.filter(tipo=4),
                   'ResultadosD': Cuenta.objects.filter(tipo=5),
                   'contraActivos': Cuenta.objects.filter(tipo=6)})


def cuenta_nueva(request):
    cuentas = CuentaForm()
    cuentaNueva = Cuenta()

    if request.method == 'POST':
        formulario = CuentaForm(request.POST)
        if formulario.is_valid():
            tipo=formulario.cleaned_data["tipo"]
            cuentaNueva.nombre = formulario.cleaned_data["nombre"]
            cuentaNueva.tipo = TipoCuenta.objects.get(id = int(tipo))

            cuentaNueva.rubro = formulario.cleaned_data["rubro"]
            rubro=cuentaNueva.rubro.numero
            cuentaNueva.codigo = str(tipo)+str(rubro)
            cuentaNueva.saldoInicial = 0
            cuentaNueva.debe = 0
            cuentaNueva.haber = 0
            cuentaNueva.saldoFinal = 0

            cuentaNueva.save()
            return cuentas_list_view(request)
        else:
            return render(request,  'main/cuentas_list.html', {'cuenta': cuentas})

    return render(request,  'main/cuentas_list.html', {'cuenta': cuentas})


def ajustes_financieros_view(request):
    return render(request, 'main/ajustes_financieros.html', {
        'titulo': 'Ajustes',
    })


def balance_general_view(request):
    return render(request, 'main/balance_general.html', {
        'titulo': 'Balance',
    })


def estado_capital_view(request):
    return render(request, 'main/estado_capital.html', {
        'titulo': 'Estado de Capital',
    })


def estado_resultados(request):
    return render(request, 'main/estado_resultados.html', {
        'titulo': 'Estado de Resultados',
    })


def balance_comprobacion(request):
    return render(request, 'main/balance_comprobacion.html', {


        'titulo': 'Balance de Comprobación','cuentas':Cuenta.objects.all()
    })


def agregar_movimiento(request):

    formulario=TransaccionForm()

    if request.method == 'POST':
        futura = int(request.POST.get('mov'))
        movimientos = formset_factory(MovimientoForm, extra=futura)

        return render(request, 'main/libro_diario.html', {'titulo': 'Libro Diario', 'movimientos': movimientos, 'transaccion': formulario, 'agregar': True})
    elif request.method == 'GET':
        return render(request, 'main/libro_diario.html')

def agregar_Transaccion(request):
    movimientoF = formset_factory(MovimientoForm)

    if request.method == 'POST':
        formulario = TransaccionForm(request.POST)
        movimientos = movimientoF(request.POST)

        if formulario.is_valid() & movimientos.is_valid():
            empleado1 = formulario.cleaned_data["empleado"]
            transaccion = Transaccion.objects.create(empleado=empleado1, monto=formulario.cleaned_data["monto"], tipo=formulario.cleaned_data["tipo"], descripcion=formulario.cleaned_data["descripcion"], fecha=formulario.cleaned_data["fecha"])

            transaccion2 = transaccion
            return guardarMovimientos(request, formulario, movimientos, transaccion2)
        return render(request, 'main/libro_diario.html', {'transaccion': formulario, 'agregar': formulario})


def libro_diario(request):
    transaccion = TransaccionForm()

    return render(request, 'main/libro_diario.html', {
        'titulo': 'Libro Diario', 'transaccion': transaccion, 'agregar': False
    })


def guardarMovimientos(request,formulario,movimientos, transaccion):
    for movimiento in movimientos:
        movimientoM = Movimiento()
        movimientoM.cuenta = movimiento.cleaned_data.get('cuenta')
        movimientoM.debe = False
        movimientoM.cantidad = movimiento.cleaned_data.get('cantidad')

        Movimiento.objects.create(cuenta=movimiento.cleaned_data.get('cuenta'), debe=movimiento.cleaned_data.get('tipo'), cantidad=movimiento.cleaned_data.get('cantidad'), transaccion=Transaccion.objects.get(id=Transaccion.objects.count()))
        cuentaModificar = Cuenta.objects.get(id=movimientoM.cuenta.id)

        cuentaModificar.save()

        if movimientoM.debe:
            cuentaModificar.debe += movimientoM.cantidad
            t=guardarCambioCuenta(cuentaModificar)
        else:
            cuentaModificar.haber += movimientoM.cantidad
            t=guardarCambioCuenta(cuentaModificar)

    return render(request, 'main/libro_diario.html', {'transaccion': formulario, 'agregar': True})


def guardarCambioCuenta(cuenta_modificar):
    if cuenta_modificar.haber >= cuenta_modificar.debe:
        cuenta_modificar.saldoFinal = cuenta_modificar.haber - cuenta_modificar.debe
        cuenta_modificar.acreedor = True
    else:
        cuenta_modificar.saldoFinal = cuenta_modificar.debe - cuenta_modificar.haber
        cuenta_modificar.acreedor = False
    cuenta_modificar.save()
    return 1


def empleado_view(reques):
    if reques.method == 'POST':
        form = EmpleadoForm(reques.POST)
        if form.is_valid():
            form.save()
            return redirect('empleados_list')
    else:
        form = EmpleadoForm()

    return render(reques, 'main/agregarEmpleado.html', {'form': form, 'titulo': 'Agregar Empleado'})


class empleado_list(ListView):
    model = Empleado
    template_name = 'main/list_empleados.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/list_empleados.html', {
            'titulo':'Empleados',
            'object_list': Empleado.objects.all()
        })



class planilla(ListView):
    model = Empleado
    template_name = 'main/Planilla.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'main/Planilla.html', {
            'titulo':'Planilla',
            'object_list': Empleado.objects.all()
        })



class listaOrdenes(ListView):
    model = ordenDeFabricacion
    template_name = 'main/ordenFabricacion.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'main/ordenFabricacion.html', {
            'titulo':'Ordenes de Fabricación',
            'object_list': ordenDeFabricacion.objects.all()
        })



class listaProductos(ListView):
    model = producto
    template_name = 'main/produccion_ventas.html'

    def get(self, request, *args, **kwargs):
        fecha = datetime.today().date()
        fecha = fecha.replace(day=1)
        productos = producto.objects.filter(ordenDeFabricacion__fechaExpedicion__year=fecha.year)\
            .filter(ordenDeFabricacion__fechaExpedicion__month=fecha.month)

        totalMP = 0.0
        invI_PenP = 0.0
        totalMOD = 0.0
        importe = 0.0
        invF_PenP = 0.0
        costoArtTerminado = 0.0
        InvI_PT = 0.0
        artTermDisp = 0.0
        InvF_PTerm = 0.0
        costoVendido = 0.0

        for p in productos:
            totalMP += p.ordenDeFabricacion.totalMP()

        for p in productos:
            totalMOD += p.ordenDeFabricacion.totalMOD()

        for p in productos:
            invI_PenP += p.invIniPenP

        for p in productos:
            InvI_PT += p.invInicialProductTerminado

        for p in productos:
            importe += p.ordenDeFabricacion.importe()

        for p in productos:
            invF_PenP += p.invFinalPenP

        for p in productos:
            costoArtTerminado += p.costoArtTerminado()

        for p in productos:
            artTermDisp += p.artTerDisp()

        for p in productos:
            invF_PenP += p.invFinalPenP

        for p in productos:
            InvF_PTerm += p.invFinalProductTerminado

        for p in productos:
            costoVendido += p.costoVendido()

        # aux = productos.aggregate(totalMP=Sum('ordenDeFabricacion__catidadMP'), totalCU=Sum('ordenDeFabricacion__costoUnitarioMP'))
        # totalMP = float(aux['totalMP'])*float(aux['totalCU'])
        # calculos = productos.aggregate(totalMOD=Sum(''))

        if len(args) > 0:
            fecha.replace(month=args.index('mes'))
            fecha.replace(args.index('año'))

        return render(request, self.template_name, {
            'titulo': 'Producción y Ventas',
            'object_list': productos,
            'totalMP': totalMP,
            'invI_PenP': invI_PenP,
            'totalMOD': totalMOD,
            'importe': importe,
            'invF_PenP': invF_PenP,
            'InvI_PT': InvI_PT,
            'costoArtTerminado': costoArtTerminado,
            'artTermDisp': artTermDisp,
            'InvF_PTerm': InvF_PTerm,
            'costoVendido': costoVendido
        })


class listaMovimientosMP(ListView):
    model = MovimientoMp
    template_name = 'main/inventarioMP.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'main/inventarioMP.html', {
            'titulo':'Inventario de materia Prima',
            'object_list': MovimientoMp.objects.all()
        })


class CrearOrde(CreateView):
    model = ordenDeFabricacion
    form_class = OrdenForm
    template_name = 'main/agregarOrden.html'
    success_url = reverse_lazy('ordenes')


class crearMovimientoMP(CreateView):
    model = MovimientoMp
    form_class = MovimientoForm
    template_name = 'main/agregarMovimientoMP.html'
    success_url = reverse_lazy('inventario')

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'main/agregarMovimientoMP.html', {'titulo':'Agregar movimiento'})





