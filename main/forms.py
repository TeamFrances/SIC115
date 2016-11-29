# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError

from main.models import ordenDeFabricacion, producto, MovimientoMp, Cliente, Proveedor
from models import Cuenta,Rubro, Empleado,TipoTransaccion

tiposCuentas=((1,'Activo',),(2,'Pasivo',),(3,'Capital',),(4,'Resultado Deudora',),(5,'Resultado Acreedora'),)
DATE_INPUT_FORMATS = '%d-%m-%Y'
debes=((1,'Debe',),(0,'Haber',))

class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'validate white-text'}))
    password = forms.CharField(required=True,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'validate white-text'}))


# class CuentaForm(forms.Form):
#     nombre = forms.CharField(required=True,
#                              label='Nombre de la cuenta')
#     rubro = forms.ModelChoiceField(required=True,
#                                    queryset=Rubro.objects.all())
#     tipo = forms.ChoiceField(required=True,
#                              choices=tiposCuentas)


class MovimientoForm(forms.Form):
    cuenta=forms.ModelChoiceField(label='Eliga la cuenta a realizar el movimiento',
        queryset=Cuenta.objects.all())


    tipo=forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'id':'test6p','checked':'checked'}),
        choices=debes
    )
    cantidad=forms.DecimalField(label='Cantidad a transferir a Cuenta:',max_digits=10,decimal_places=2,min_value=0)


class TransaccionForm(forms.Form):
    # monto=forms.DecimalField(label='monto de transaccion',max_digits=10, decimal_places=2,min_value=0.0)
    empleado=forms.ModelChoiceField(required=True,
            queryset=Empleado.objects.all())
    tipo=forms.ModelChoiceField(required=True,
            queryset=TipoTransaccion.objects.all())
    descripcion=forms.CharField(widget=forms.Textarea)

    fecha=forms.DateField()


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado

        fields=[
            'nombres',
            'apellidos',
            'edad',
            'sexo',
            'direccion',
            'telefono',
            'contacto',
            'dui',
            'nit',
            'afp',
            'puesto',
            'activo',
        ]
        labels={
            'nombres': 'Nombres',
            'apellidos':'Apellidos',
            'edad': 'Edad',
            'sexo': 'sexo',
            'direccion':'Direccion',
            'telefono':'telefono',
            'contacto':'Contacto',
            'dui':'DUI',
            'nit':'NIT',
            'afp':'AFP',
            'puesto':'Puesto',
            'activo':'Activo',
        }
        widgets={
            'nombres': forms.TextInput (attrs={'class':'input-field col s3'}),
            'apellidos':forms.TextInput (attrs={'class':'input-field '}),
            'edad':forms.NumberInput(attrs={'class':'input-field '}),
            'sexo':forms.Select(attrs={'class':'input-field '}),
            'direccion':forms.TextInput (attrs={'class':'input-field'}),
            'telefono':forms.NumberInput (attrs={'class':'input-field '}),
            'contacto':forms.TextInput (attrs={'class':'input-field'}),
            'dui':forms.TextInput (attrs={'class':'input-field '}),
            'nit':forms.TextInput (attrs={'class':'input-field '}),
            'afp':forms.TextInput (attrs={'class':'input-field'}),
            'puesto':forms.Select(attrs={'class':'input-field'}),
            'activo':forms.CheckboxSelectMultiple(attrs={'type':'checkbox'}),
        }

    def clean_nombres(self):
        nombres = self.cleaned_data['nombres']

        if not (nombres.isalpha()):
            raise ValidationError("Los nombres no deben contener números")

        return nombres


class EquipoForm(forms.Form):
    nombre=forms.CharField(required=True, label="Ingrese el nombre del equipo a comprar",widget=forms.TextInput(attrs={'class':'input-field'}))
    vida_util=forms.IntegerField(required=True,label="Ingrese la vida util del dispositivo", min_value=1)
    valor_de_compra=forms.DecimalField(label="ingrese el valor de compra", min_value=0)
    recuperacion=forms.DecimalField(label="Ingrese el valor de recuperacion", min_value=0)




class ProductoForm(forms.ModelForm):
    class Meta:
        model = producto

        fields=['nombre', 'ordenDeFabricacion', 'nuneroArticulos',]


class OrdenForm(forms.ModelForm):
    class Meta:
        model = ordenDeFabricacion

        fields = [
            'cliente',
            'fechaExpedicion',
            'fechaRequerida',
            'materal',
            'catidadMP',
            'costoUnitarioMP',
            'obrero',
            'numHoras',
            'costoHora',
            'tasaCIF',

        ]
        labels = {
            'FechaExpedicion':'Fecha de expedición',
            'fechaRequerida':'Fecha requerida',
            'materal':'Material',
            'catidadMp':'Cantidad de Material',
            'costoUnitarioMP':'Costo Unitario',
            'obrero':'Empleado',
            'numHoras':'Numero de horas',
            'costoHora':'Costo por hora',
            'tasaCIF':'Tasa CIF',

        }
        widgets = {
            'fechaExpedicion': forms.TextInput(attrs={'class': 'input-field '}),
            'fechaRequerida': forms.TextInput(attrs={'class': 'input-field '}),
            'materal':forms.TextInput(attrs={'class': 'input-field '}),
            'catidadMP':forms.NumberInput(attrs={'class': 'input-field '}),
            'costoUnitarioMP': forms.NumberInput(attrs={'class': 'input-field '}),
            'obrero': forms.Select(attrs={'class': 'input-field '}),
            'numHoras': forms.NumberInput(attrs={'class': 'input-field '}),
            'costoHora': forms.NumberInput(attrs={'class': 'input-field '}),
            'tasaCIF': forms.NumberInput(attrs={'class': 'input-field '}),
        }


class MovimientoFormMP(forms.ModelForm):
    class Meta:
        model = MovimientoMp

        fields=['proveedor','fecha', 'nombre', 'cantidad', 'precioUnitario','tipo']


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta

        fields = ['nombre', 'rubro', 'tipo']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor

        fields = ['marca', 'direccion', 'telefono', 'nit']