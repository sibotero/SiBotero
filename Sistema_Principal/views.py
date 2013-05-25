# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render, HttpResponse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from Sistema_Principal.models import Empresa,Cliente,Moto, T_financiacion,Cotizacion,Medio_Publicitario, Matricula,CotizacionFila,Kit
from Sistema_Principal.forms import CotizacionMaestro
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from Sistema_Principal.forms import AgregarCliente
from datetime import date
from Sistema_Principal.html2pdf import converter as html2pdf
from io import BytesIO
from django import forms
from django.core import mail
from django.forms.formsets import formset_factory


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
            return render_to_response("cotizador/cotizador.html",{'form':form,'inline':0},context_instance=RequestContext(request))
        if request.method == "POST":
            empresa = request.session['enterprise']
            form = CotizacionMaestro(request.POST)
            if form.is_valid():
                n_childs = int(request.POST['rows'])
                errors = []
                for i in range(n_childs):
                    moto = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                    cuota_inicial =  int(request.POST['cuota_inicial_'+str(i+1)])
                    n_cuotas = request.POST.getlist('n_cuotas_'+str(i+1))
                    kit = Kit.objects.filter(empresa=empresa).get(moto_asociada=moto)
                    if moto.cuota_minima > cuota_inicial:
                        errors.append("La cuota de la moto "+moto.referencia+" "+moto.modelo+" debe ser mayor a "+str(moto.cuota_minima))
                    if len(n_cuotas)<1:
                        errors.append("Debe elegir por lo menos 1 numero de cuotas para la moto "+moto.referencia+" "+moto.modelo)
                    if cuota_inicial > (moto.precio_publico + kit.totalkit()):
                        errors.append("La cuota inicial sobrepasa el valor a pagar para la moto "+moto.referencia+" "+moto.modelo)
                if(len(errors)>=1):
                    #generar el html con los errores y los valores seleccionados
                    form = CotizacionMaestro(request.POST)
                    table = ""
                    clientes = Cliente.objects.filter(empresa=empresa)
                    for i in range(n_childs):
                        motosel = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                        cuota_inicial =  int(request.POST['cuota_inicial_'+str(i+1)])
                        sn_cuotas = request.POST.getlist('n_cuotas_'+str(i+1))
                        print sn_cuotas
                        empresa = request.session['enterprise']
                        motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
                        n_cuotas = T_financiacion.objects.filter(empresa=empresa)
                        table += render_to_string("cotizador/inline_fila_cotizacion.html",{'numero_inline':(i+1),'motos':motos,'cuotas':n_cuotas,'cinicial':cuota_inicial,'motosel':motosel,'sncuotas':sn_cuotas,'is_inerror':True})
                    return render_to_response("cotizador/cotizador.html",{'form':form,'inline':n_childs,'contenttable':table,'errors':errors,'is_inerror':True},context_instance=RequestContext(request))
                else:
                    cot_maestra = form.save(commit=False)
                    cot_maestra.numeracion = Cotizacion.objects.filter(empresa=empresa).count()+1
                    cot_maestra.fecha_cot = date.today()
                    cot_maestra.vendedor = request.user
                    cot_maestra.empresa = request.session['enterprise']
                    cot_maestra.save()
                    for i in range(n_childs):
                        cuota_inicial = int(request.POST['cuota_inicial_'+str(i+1)])
                        moto = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                        n_no_aplicables = 0
                        matricula_asociada = Matricula.objects.filter(empresa=empresa,nombre_ciudad=request.user.ciudad)[0]
                        lista=request.POST.getlist('n_cuotas_'+str(i+1))
                        cot = CotizacionFila()
                        cot.cotizacion = cot_maestra
                        cot.moto = moto
                        cot.cuota_inicial = cuota_inicial
                        cot.n_no_aplicables = n_no_aplicables
                        cot.matricula_asociada = matricula_asociada
                        cot.save()
                        for i in range(len(lista)):
                            reg = T_financiacion.objects.get(empresa=empresa,num_meses=lista[i])
                            cot.n_cuotas.add(reg)
                        cot.save()
                    return HttpResponseRedirect("/reporte/")
            else:
                form = CotizacionMaestro(request.POST)
                table = ""
                clientes = Cliente.objects.filter(empresa=empresa)
                n_childs =int(request.POST['rows'])
                for i in range(n_childs):
                    motosel = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                    cuota_inicial =  int(request.POST['cuota_inicial_'+str(i+1)])
                    sn_cuotas = request.POST.getlist('n_cuotas_'+str(i+1))
                    empresa = request.session['enterprise']
                    motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
                    n_cuotas = T_financiacion.objects.filter(empresa=empresa)
                    table += render_to_string("cotizador/inline_fila_cotizacion.html",{'numero_inline':(i+1),'motos':motos,'cuotas':n_cuotas,'cinicial':cuota_inicial,'motosel':motosel,'cselec':sn_cuotas,'is_inerror':True})
                return render_to_response("cotizador/cotizador.html",{'form':form,'inline':n_childs,'contenttable':table,'errors':[]},context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect("/login/")

def get_row(request,n_inline):
    if request.method == "GET":
            empresa = request.session['enterprise']
            motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
            n_cuotas = T_financiacion.objects.filter(empresa=empresa)
            return render_to_response("cotizador/inline_fila_cotizacion.html",{'numero_inline':n_inline,'motos':motos,'cuotas':n_cuotas,'cinicial':0,'is_inerror':False})