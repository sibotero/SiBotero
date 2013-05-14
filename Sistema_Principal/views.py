# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render
from django.template.context import RequestContext
from Sistema_Principal.models import Empresa,Cliente,Moto, T_financiacion
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from Sistema_Principal.forms import AgregarCliente
from django.http import HttpResponse


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
            print empresa+" "+username+" "+password
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
                        print "bienvenido administrador"
                        return redirect("/admin/",context_instance= RequestContext(request))
                    elif not user.es_admin:
                        print "bienvenido usuario"
                        return redirect("/cotizacion/",context_instance= RequestContext(request))
                else:
                    error = "Usuario/Empresa no validos"
                    return render_to_response("login.html",{'empresas':empresas , 'error_message':error},context_instance= RequestContext(request))
            else:
                error = "Usuario/Contraseña no validos"
                return render_to_response("login.html",{'empresas':empresas , 'error_message':error},context_instance= RequestContext(request))
    else:
        return render_to_response("login.html",{'empresas':empresas},context_instance= RequestContext(request))

def cotizacion(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    usuario = request.user
    empresa = request.session['enterprise']
    print usuario.nombre
    clientes = Cliente.objects.filter(empresa=empresa.id)
    clientes.order_by('-id')
    motos = list(Moto.objects.filter(inventario_motos__en_venta=True))
    tasas = T_financiacion.objects.filter(empresa=empresa.id)

    return render_to_response("cotizador/cotizador.html",{'clientes':clientes,'motos':motos,'tasas':tasas},context_instance= RequestContext(request))


def logout(request):
    auth_logout(request)
    return redirect("/login/")

def add_cliente(request):
    if request.method == "GET":
        print "AQUI"
        form_add = AgregarCliente()
        print (form_add.as_p())
        return render_to_response("cotizador/form_cliente.html",{'form':form_add},context_instance=RequestContext(request))
    elif request.method =="POST":
        form = AgregarCliente(request.POST)
        if form.is_valid():
            print "AQUI!!"
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            not_por_email = form.cleaned_data['not_por_email']
            cliente = Cliente()
            cliente.cedula = cedula
            cliente.nombre = nombre
            cliente.apellidos = apellidos
            cliente.direccion = direccion
            cliente.telefono = telefono
            cliente.email = email
            cliente.not_por_email = not_por_email
            cliente.empresa = request.session['enterprise']
            cliente.save()
            return HttpResponseRedirect("/cotizacion/")
        else:
            return render(request,"cotizador/form_cliente.html",{'form':form},context_instance=RequestContext(request),status="400")
            #return render_to_response("cotizador/form_cliente.html",{'form':form},context_instance=RequestContext(request))

