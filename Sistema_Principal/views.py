# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import RequestContext
from Sistema_Principal.models import Empresa,Cliente,Moto, T_financiacion
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


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
    clientes = list(Cliente.objects.filter(empresa=empresa.id))
    motos = list(Moto.objects.filter(inventario_motos__en_venta=True))
    tasas = T_financiacion.objects.filter(empresa=empresa.id)
    return render_to_response("cotizador/base.html",{'clientes':clientes,'motos':motos,'tasas':tasas},context_instance= RequestContext(request))


def logout(request):
    auth_logout(request)
    return redirect("/login/")