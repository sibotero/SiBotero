# -*- encoding: utf-8 -*-
from django import forms
from Sistema_Principal.models import Cotizacion,Moto,Empresa

class AgregarCliente(forms.Form):
    cedula = forms.IntegerField(help_text=("Cedula del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    nombre = forms.CharField(max_length=20,help_text=("Nombre del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    apellidos = forms.CharField(max_length=40,help_text=("Apellidos del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    direccion = forms.CharField(max_length=200,help_text=("Direccion de Cliente"),required=True, widget=forms.Textarea)
    telefono = forms.CharField(max_length=10, help_text=("Telefono del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    email = forms.EmailField(max_length=60, help_text=("Correo del cliente"),required=True)
    not_por_email = forms.BooleanField(required=False)

class CotizarForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        exclude=['empresa','fecha_cot','vendedor']

    def clean_cuota_inicial(self):
        data = self.cleaned_data['cuota_inicial']
        minima = self.cleaned_data['moto']
        if(data < minima.cuota_minima):
            raise forms.ValidationError("La cuota minima para la Moto seleccionada es : "+str(minima.cuota_minima))
        return data

    def clean_n_cuotas(self):
        moto = self.cleaned_data['moto']
        empresa = Empresa.objects.get(id = moto.empresa_id)
        vip = self.cleaned_data['no_aplicables']
        data = self.cleaned_data['n_cuotas']
        print data
        for t in data:
            if vip and t.num_meses > empresa.cuotas_no_aplic:
                raise forms.ValidationError("Si se es VIP no puede tener cuotas mayores a "+str(empresa.cuotas_no_aplic))
        return data