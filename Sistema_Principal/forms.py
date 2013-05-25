# -*- encoding: utf-8 -*-
from django import forms
from Sistema_Principal.models import Cotizacion,Moto,Empresa,Cliente,Medio_Publicitario,CotizacionFila

class AgregarCliente(forms.Form):
    cedula = forms.IntegerField(help_text=("Cedula del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    nombre = forms.CharField(max_length=20,help_text=("Nombre del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    apellidos = forms.CharField(max_length=40,help_text=("Apellidos del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    direccion = forms.CharField(max_length=200,help_text=("Direccion de Cliente"),required=True, widget=forms.Textarea)
    telefono = forms.CharField(max_length=10, help_text=("Telefono del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    email = forms.EmailField(max_length=60, help_text=("Correo del cliente"),required=True)
    not_por_email = forms.BooleanField(required=False)

class CotizacionMaestro(forms.ModelForm):
    class Meta:
        model = Cotizacion
        exclude = ['empresa','fecha_cot','vendedor','numeracion']

    def cleanned_cliente(self):
        value = self.cleaned_data['cliente']
        data = Cliente.objects.get(id=value)
        if data != None:
            return value
        else:
            raise forms.ValidationError("No puede dejar el campo cliente en blanco")

    def cleaned_medio(self):
        value = self.cleaned_data['medio']
        data = Medio_Publicitario.objects.get(id=value)
        if data != None:
            return value
        else:
            raise forms.ValidationError("¿Por que medio se entero el cliente?")
