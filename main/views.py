# coding: utf-8

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView

from main.forms import LoginForm, TransaccionForm, CuentaForm
from main.models import Transaccion, Cuenta, TipoCuenta


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
    return render(request,  'main/cuentas_list.html', {
        'cuenta': cuentas,
        'titulo': 'Cuentas',
        'activos': Cuenta.objects.filter(tipo=1),
        'pasivos': Cuenta.objects.filter(tipo=2),
        'patrimonios': Cuenta.objects.filter(tipo=3),
        'resultadosA': Cuenta.objects.filter(tipo=4),
        'ResultadosD': Cuenta.objects.filter(tipo=5),
        'contraActivos': Cuenta.objects.filter(tipo=6)
      })


def cuenta_nueva(request):
    cuentas=CuentaForm()
    cuentaNueva=Cuenta()
    if request.method=='POST':
        formulario=CuentaForm(request.POST)
        if formulario.is_valid():
            tipo=formulario.cleaned_data["tipo"]
            cuentaNueva.nombre=formulario.cleaned_data["nombre"]
            cuentaNueva.tipo=TipoCuenta.objects.get(id=int(tipo))

            cuentaNueva.rubro=formulario.cleaned_data["rubro"]
            rubro=cuentaNueva.rubro.numero
            cuentaNueva.codigo=str(tipo)+str(rubro)
            cuentaNueva.saldoInicial=0
            cuentaNueva.debe=0
            cuentaNueva.haber=0
            cuentaNueva.saldoFinal=0

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
        'titulo': 'Balance de Comprobación',
    })


# def libro_diario(request):
#     return render(request, 'main/libro_diario.html', {
#         'titulo': 'Libro Diario',
#     })


class TransaccionCreateView(CreateView):
    model = Transaccion
    template_name = 'main/libro_diario.html'
    form_class = TransaccionForm
    success_url = reverse_lazy('libro_diario')
