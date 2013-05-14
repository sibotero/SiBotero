# -*- encoding: utf-8 -*-
from django import forms
from django.utils.html import format_html
class email_widget(forms.Widget):
    def render(self, name, value, attrs=None):
        return format_html('<input name="'+name+'" type="email" id="id_email" value=""/>')

class AgregarCliente(forms.Form):
    cedula = forms.IntegerField(help_text=("Cedula del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    nombre = forms.CharField(max_length=20,help_text=("Nombre del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    apellidos = forms.CharField(max_length=40,help_text=("Apellidos del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    direccion = forms.CharField(max_length=200,help_text=("Direccion de Cliente"),required=True, widget=forms.Textarea)
    telefono = forms.CharField(max_length=10, help_text=("Telefono del Cliente"),required=True,widget=forms.TextInput(attrs={'class':'required'}))
    email = forms.EmailField(max_length=60, help_text=("Correo del cliente"),required=True,widget=email_widget())
    not_por_email = forms.BooleanField(required=False)

