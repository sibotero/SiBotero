# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render, HttpResponse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from Sistema_Principal.models import Empresa,Cliente,Moto, T_financiacion,Cotizacion,Medio_Publicitario, Matricula
from Sistema_Principal.forms import CotizacionMaestro
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from Sistema_Principal.forms import AgregarCliente
#from Sistema_Principal.forms import CotizarForm
from Sistema_Principal.html2pdf import converter as html2pdf
from io import BytesIO
from django import forms
from django.core import mail



def login(request):
    empresas = Empresa.objects.all()
    if request.user.is_authenticated():
        if request.user.es_admin:
            return redirect("/admin/")
        else:
            return redirect("/cotizacion/")
    if request.method == 'POST':
            empresa = request.POST['enterprise']
            username = request.POST['username']
            password = request.POST['password']
            #print empresa+" "+username+" "+password
            user = authenticate(username=username,password=password)
            if not user==None:
                empresasusr = list(user.empresa.all())
                objemp = Empresa.objects.get(pk=empresa)

                if objemp in empresasusr:
                    print "aqui aqui"
                    try:
                        url_image = objemp.imagen.url
                    except:
                        url_image = None
                    request.session['url_image']=url_image
                    request.session['user_enterprise'] = objemp.id
                    request.session['enterprise'] = objemp
                    auth_login(request, user)
                    print "usuario logeado"
                    if user.es_admin:
                        #print "bienvenido administrador"
                        return redirect("/admin/",context_instance= RequestContext(request))
                    elif not user.es_admin:
                        #print "bienvenido usuario"
                        return redirect("/cotizacion/",context_instance= RequestContext(request))
                else:
                    error = "Usuario/Empresa no validos"
                    return render_to_response("login.html",{'empresas':empresas , 'error_message':error},context_instance= RequestContext(request))
            else:
                error = "Usuario/Contraseña no validos"
                return render_to_response("login.html",{'empresas':empresas , 'error_message':error},context_instance= RequestContext(request))
    else:
        return render_to_response("login.html",{'empresas':empresas},context_instance= RequestContext(request))

def logout(request):
    auth_logout(request)
    return redirect("/login/")

def cotizacion(request):
    print request.user
    if request.user.is_authenticated():
        if request.method == "GET":
            empresa = request.session['enterprise']
            form = CotizacionMaestro()
            clientes = Cliente.objects.filter(empresa=empresa)
            medios = Medio_Publicitario.objects.filter(empresa=empresa)
            form['cliente'].queryset = clientes
            form['medio'].queryset = medios
            print form.as_table()
            return render_to_response("cotizador/cotizador.html",{'clientes':clientes,'form':form},context_instance=RequestContext(request))
        if request.method == "POST":
            print "HOLA MUNDO"
            pass
    else:
        return HttpResponseRedirect("/login/")

def get_row(request,n_inline):
    if request.method == "GET":
            empresa = request.session['enterprise']
            motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
            n_cuotas = T_financiacion.objects.filter(empresa=empresa)
            return render_to_response("cotizador/inline_fila_cotizacion.html",{'numero_inline':n_inline,'motos':motos,'cuotas':n_cuotas})