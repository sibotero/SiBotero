# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render, HttpResponse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from Sistema_Principal.models import Empresa,Cliente,Moto, T_financiacion,Cotizacion,Medio_Publicitario, Matricula
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from Sistema_Principal.forms import AgregarCliente
from Sistema_Principal.forms import CotizarForm
from Sistema_Principal.html2pdf import converter as html2pdf
from io import BytesIO
from django import forms
from django.core import mail
from django.utils import simplejson
from datetime import datetime


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

def cotizacion(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    usuario = request.user
    empresa = request.session['enterprise']
    clientes = Cliente.objects.all().filter(empresa=empresa).order_by('-id')
    print clientes
    motos = Moto.objects.filter(inventario_motos__en_venta=True).filter(empresa=empresa)
    medios_pub = Medio_Publicitario.objects.filter(empresa=empresa)
    tasas = T_financiacion.objects.filter(empresa=empresa)
    matriculas = Matricula.objects.filter(empresa = empresa)
    if request.method == "GET":
        form = CotizarForm()
        form.fields['cliente'].queryset = clientes
        form.fields['moto'].queryset = motos
        form.fields['n_cuotas'].queryset = tasas
        form.fields['medio'].queryset = medios_pub
        form.fields['matricula_asociada'].queryset = matriculas
        #print form.as_table()
        return render_to_response("cotizador/cotizador.html",{'clientes':clientes,'motos':motos,'tasas':tasas,'form':form},context_instance= RequestContext(request))
    if request.method=="POST":
        form = CotizarForm(request.POST)
        form.fields['cliente'].queryset = clientes
        form.fields['moto'].queryset = motos
        form.fields['n_cuotas'].queryset = tasas
        form.fields['medio'].queryset = medios_pub
        form.fields['matricula_asociada'].queryset = matriculas
        form.fields['cliente'] = forms.ModelChoiceField(clientes,)
        if form.is_valid():
            add = form.save(commit=False)
            add.fecha_cot = datetime.today()
            add.empresa = request.session['enterprise']
            add.vendedor = request.user
            add.n_no_aplicables = request.session['enterprise'].cuotas_no_aplic
            add.save()
            form.save_m2m()
            return HttpResponseRedirect("/reportar/%s/"%(add.id))
        else:
            return render_to_response("cotizador/cotizador.html",{'clientes':clientes,'motos':motos,'tasas':tasas,'form':form},context_instance= RequestContext(request))


def report_cot(request,id_cot):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    ctx = get_dic_to_report(request,id_cot)

    return render_to_response("cotizador/reporte.html",ctx,context_instance=RequestContext(request))


def report_cot_pdf(request,id_cot):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    filename = "temp"+str(datetime.now())+".pdf"
    buffer = BytesIO()

    ctx = get_dic_to_report(request,id_cot)

    """ Aca se traera la informacion en html del resultado y se escribira en
    el pdf
    """
    #print request.session['enterprise'].imagen.path
    return html2pdf.render_to_pdf("cotizador/pdf_report.html",ctx,pdfname=str(datetime.now())+".pdf")

def logout(request):
    auth_logout(request)
    return redirect("/login/")

def add_cliente(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    if request.method == "GET":
        #print "AQUI"
        form_add = AgregarCliente()
        #print (form_add.as_p())
        return render_to_response("cotizador/form_cliente.html",{'form':form_add},context_instance=RequestContext(request))
    elif request.method =="POST":
        form = AgregarCliente(request.POST)
        if form.is_valid():
            #print "AQUI!!"
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
            return HttpResponseRedirect("/thanks/")
        else:
            return render(request,"cotizador/form_cliente.html",{'form':form},context_instance=RequestContext(request))
            #return render_to_response("cotizador/form_cliente.html",{'form':form},context_instance=RequestContext(request))

def gracias(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    return render_to_response("cotizador/thanks.html",{},context_instance=RequestContext(request))

def pdf_a_mail(request,id_cot):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    cot = Cotizacion.objects.get(id = id_cot)
    if cot != None:
        email = cot.cliente.email
        empresa = request.session['enterprise']
        subject = 'Cotizacion en '+empresa.nombre+' '+str(datetime.today())
        body = unicode("\n"+"\n"+"Este mensaje fue autogenerado por el sistema. Por favor no contestar este mensaje\n"+ "Empresa : "+empresa.nombre+" Telefono: "+empresa.telefono+" Correo:"+empresa.correo+"\n"+"Direccion : "+empresa.direccion+"         \n"+"NIT: "+empresa.nit+"  Ciudad: "+empresa.ciudad+".")
        efrom = "sicobotero@hotmail.com"
        ctx = get_dic_to_report(request,id_cot)
        file_att = html2pdf.info_to_pdf("cotizador/pdf_report.html",ctx,pdfname=str(datetime.now())+".pdf")
        #print file_att.content.decode("windows-1252")
        message = mail.EmailMessage(subject,body,efrom,to=[email,],headers = {'Reply-To': efrom})
        message.attach("Reporte.pdf",file_att.content,mimetype="application/pdf")
        message.send()
        return HttpResponseRedirect('/reportar/'+str(id_cot)+"/")
        pass
    else:
        return HttpResponse(status=404)
    pass

def get_dic_to_report(request,id_cot):
    cot = Cotizacion.objects.get(id=id_cot)
    moto = cot.moto.precio_publico
    moto_obj = Moto.objects.get(pk = cot.moto.id)
    kit = cot.moto.kit_set.all()[0]
    kit_total = kit.casco + kit.chaleco + kit.placa + kit.soat + kit.transporte
    n_cuotas = cot.n_cuotas.all()[0:]
    m_asociadas = cot.matricula_asociada.all()[0:]
    c_ini = cot.cuota_inicial
    sin_mat = moto + kit_total
    l_con_mat = []
    for i,mat in enumerate(m_asociadas):
        #print i
        l_con_mat.append( (sin_mat+mat.precio) - c_ini )
    #print l_con_mat
    l_preciot_cuotas = []

    for i,el in enumerate(l_con_mat):
        l_preciot_cuotas.append([])
        for j,fin in enumerate(n_cuotas):
            if cot.no_aplicables:
                l_preciot_cuotas[i].append(int(el/fin.num_meses))
            else:
                if fin.valor_por != 0:
                    l_preciot_cuotas[i].append(int(el*fin.valor_por))
                else:
                    l_preciot_cuotas[i].append(int(el/fin.num_meses))

    #print l_preciot_cuotas

    return{
        'cot':cot, 'precio_moto':moto, 'objmoto':moto_obj,'kit':kit,'precio_kit':kit_total,
        'n_cuotas':n_cuotas,'m_asociadas':m_asociadas,'cuota_inicial':c_ini,'precio_con_kit':sin_mat,
        'precio_con_matriculas':l_con_mat,'lista_total_cotizada':l_preciot_cuotas,'request':request,'id_cot':id_cot,
        'user':request.user
    }

def is_vip(request,id_cli):
    to_json = {'vip':Cliente.objects.get(id=id_cli).es_vip,}
    json = simplejson.dumps(to_json)
    #print json
    return HttpResponse(json,mimetype="application/json")

def impacto_medios(request):
    if request.user.is_authenticated and request.user.is_staff:
        medios = Medio_Publicitario.objects.filter(empresa= request.session['enterprise'])
        return render_to_response('cotizador/reportes_medios.html',{'medios':medios},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login/")

def get_last_cliente(request):
    if request.user.is_authenticated:
        empresa = request.session['enterprise']
        clientes = list(Cliente.objects.filter(empresa = empresa).order_by("-id"))
        cliente =  clientes[0]
        json = "<option value='"+cliente.id+"'>"+cliente.nombre+" "+cliente.apellidos+" : "+cliente.cedula+"</option>"
        return HttpResponse(json,mimetype="text/plain")
    else:
        HttpResponseRedirect("/login/")