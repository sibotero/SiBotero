# -*- encoding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect, render, HttpResponse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from Sistema_Principal.models import *
from Sistema_Principal.forms import CotizacionMaestro
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from Sistema_Principal.forms import AgregarCliente
from datetime import date
from wkhtmltopdf.views import PDFTemplateResponse
from Sistema_Principal.html2pdf import converter
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
                    try:
                        url_image = objemp.imagen.url
                    except:
                        url_image = None
                    request.session['url_image']=url_image
                    request.session['user_enterprise'] = objemp.id
                    request.session['enterprise'] = objemp
                    auth_login(request, user)

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
    if request.user.is_authenticated():
        if request.method == "GET":
            empresa = request.session['enterprise']
            form = CotizacionMaestro()
            clientes = Cliente.objects.filter(empresa=empresa).order_by("-id")
            medios = Medio_Publicitario.objects.filter(empresa=empresa)
            form.fields['cliente'].queryset = clientes
            form.fields['medio'].queryset = medios

            return render_to_response("cotizador/cotizador.html",{'form':form,'inline':0},context_instance=RequestContext(request))
        if request.method == "POST":
            empresa = request.session['enterprise']
            form = CotizacionMaestro(request.POST)
            if form.is_valid():
                n_childs = int(request.POST['rows'])
                errors = []
                for i in range(n_childs):
                    tipo = int(request.POST['id_tipo_'+str(i+1)])
                    if tipo==1:
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
                if (len(errors)>=1):
                    #generar el html con los errores y los valores seleccionados
                    form = CotizacionMaestro(request.POST)
                    clientes = Cliente.objects.filter(empresa=empresa).order_by("-id")
                    medios = Medio_Publicitario.objects.filter(empresa=empresa)
                    form.fields['cliente'].queryset = clientes
                    form.fields['medio'].queryset = medios
                    table = ""
                    clientes = Cliente.objects.filter(empresa=empresa)
                    for i in range(n_childs):
                        motosel = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                        cuota_inicial =  0
                        tipo_n = int(request.POST['id_tipo_'+str(i+1)])
                        sn_cuotas = []
                        if tipo_n==1:
                            cuota_inicial =  int(request.POST['cuota_inicial_'+str(i+1)])
                            n_cuotas = request.POST.getlist('n_cuotas_'+str(i+1))

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
                        tipo = int(request.POST['id_tipo_'+str(i+1)])
                        if tipo == 1:
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
                            cot.tipo = "credito"
                            cot.save()
                            for i in range(len(lista)):
                                reg = T_financiacion.objects.get(empresa=empresa,id=lista[i])
                                cot.n_cuotas.add(reg)
                            cot.save()
                        else:
                            cuota_inicial = 0
                            moto = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                            n_no_aplicables = 0
                            matricula_asociada = Matricula.objects.filter(empresa=empresa,nombre_ciudad=request.user.ciudad)[0]
                            cot = CotizacionFila()
                            cot.cotizacion = cot_maestra
                            cot.moto = moto
                            cot.cuota_inicial = 0
                            cot.n_no_aplicables= n_no_aplicables
                            cot.matricula_asociada = matricula_asociada
                            cot.tipo = "contado"
                            req = request.POST.getlist('requisitos')
                            cot.save()
                            cot_maestra.save()
                            if (len(req)>0):
                                for r in req:
                                    a = RequisitoTabla.objects.get(id = r)
                                    cot_maestra.requisitos.add(a)
                            cot_maestra.save()
                    return HttpResponseRedirect("/reporte/"+str(cot_maestra.id)+"/")
            else:
                form = CotizacionMaestro(request.POST)
                table = ""
		empresa = request.session['enterprise']
                clientes = Cliente.objects.filter(empresa=empresa)
                medios = Medio_Publicitario.objects.filter(empresa = empresa)
                form.fields['cliente'].queryset = clientes
                form.fields['medio'].queryset = medios
                n_childs =int(request.POST['rows'])
                for i in range(n_childs):
                    motosel = Moto.objects.get(id= int(request.POST['moto_'+str(i+1)]))
                    tipo = int(request.POST['id_tipo_'+str(i+1)])
                    cuota_inicial = 0
                    sn_cuotas = []
                    if tipo == 1:
                        cuota_inicial =  int(request.POST['cuota_inicial_'+str(i+1)])
                        sn_cuotas = request.POST.getlist('n_cuotas_'+str(i+1))
                    empresa = request.session['enterprise']
                    motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
                    n_cuotas = T_financiacion.objects.filter(empresa=empresa)
                    table += render_to_string("cotizador/inline_fila_cotizacion.html",{'numero_inline':(i+1),'motos':motos,'cuotas':n_cuotas,'cinicial':cuota_inicial,'motosel':motosel,'cselec':sn_cuotas,'is_inerror':True})
                return render_to_response("cotizador/cotizador.html",{'form':form,'inline':n_childs,'contenttable':table,'errors':[],'is_inerror':True},context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect("/login/")

def get_row(request,n_inline):
    if request.method == "GET":
            empresa = request.session['enterprise']
            motos = Moto.objects.filter(empresa=empresa).filter(inventario_motos__en_venta=True)
            n_cuotas = T_financiacion.objects.filter(empresa=empresa)
            return render_to_response("cotizador/inline_fila_cotizacion.html",{'numero_inline':n_inline,'motos':motos,'cuotas':n_cuotas,'cinicial':0,'is_inerror':False})

def add_cliente(request):
    if request.user.is_authenticated():
        if request.method == "GET":
            formcliente = AgregarCliente()
            return render_to_response("cotizador/form_cliente.html",{'form':formcliente},context_instance=RequestContext(request))
        if request.method == "POST":
            formcliente = AgregarCliente(request.POST)
            if formcliente.is_valid():
                c = Cliente()
                c.cedula = formcliente.cleaned_data['cedula']
                c.nombre = formcliente.cleaned_data['nombre']
                c.apellidos = formcliente.cleaned_data['apellidos']
                c.direccion = formcliente.cleaned_data['direccion']
                c.telefono = formcliente.cleaned_data['telefono']
                c.email = formcliente.cleaned_data['email']
                c.not_por_email = formcliente.cleaned_data['not_por_email']
                c.es_vip = False
                c.empresa = request.session['enterprise']
                c.save()
                return render_to_response("cotizador/thanks.html",{},context_instance=RequestContext(request))
            else:
                return render_to_response("cotizador/form_cliente.html",{'form':formcliente},context_instance=RequestContext(request))

def report(request,id_cot):
    cot = Cotizacion.objects.get(id = int(id_cot))
    empresa = request.session['enterprise']
    cotrows = CotizacionFila.objects.filter(cotizacion = cot.id)
    cotrows_cont = cotrows.filter(tipo="contado")
    cotrows_credito = cotrows.filter(tipo="credito")
    matricula = Matricula.objects.filter(empresa=empresa,nombre_ciudad=request.user.ciudad)[0]
    tablas = ""
    tablas +="<table><thead><tr><td>Moto</td>" \
             "<td>Precio Publico</td><td>Precio KIT</td></tr></thead><tbody>"
    for i in range(cotrows.count()):
        moto = cotrows[i].moto
        tablas+="<tr><td>"+moto.referencia+" "+moto.modelo+"</td><td>"+str(moto.precio_publico)+"</td><td>"+str(Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit())+"</td></tr>"
    if cotrows_cont.count() > 0:
        tablas += "<table><thead><tr><td>Moto</td>" \
             "<td>Total Moto</td></tr></thead><tbody>"
    for i in range(cotrows_cont.count()):
        moto = cotrows_cont[i].moto
        tablas+="<tr><td>"+moto.referencia+" "+moto.modelo+"</td>"
        total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit()+matricula.precio
        tablas+="<td>"+str(total_moto)+"</td></tr>"
    tablas+="</tbody></table>"
    for i in range(cotrows_credito.count()):
        n_cuotas = cotrows_credito[i].n_cuotas.count()
        moto = cotrows_credito[i].moto
        total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit(conprenda=True)+matricula.precio
        tablas += "<br><table><thead><tr><td>Moto</td>"
        for j in range(n_cuotas):
            tablas+="<td>"+str(cotrows_credito[i].n_cuotas.all()[j].num_meses)+" cuotas</td>"
        tablas+="</tr></thead><tbody><tr><td>%s %s</td>"%(moto.referencia,moto.modelo)
        for j in range(n_cuotas):
            tablas+="<td>"+str(((total_moto-cotrows_credito[i].cuota_inicial)*(cotrows_credito[i].n_cuotas.all()[j].valor_por)))+"</td>"
        tablas+="</tr></tbody></table>"
    requisitos = cot.requisitos.all()
    return render_to_response("cotizador/reporte.html",{'tablas':tablas,'cot':cot,'requisitos':requisitos},context_instance=RequestContext(request))

def reportpdf(request,id_cot):
    cot = Cotizacion.objects.get(id = int(id_cot))
    if cot != None:
        empresa = request.session['enterprise']
        cotrows = CotizacionFila.objects.filter(cotizacion = cot.id)
        cotrows_cont = cotrows.filter(tipo="contado")
        cotrows_credito = cotrows.filter(tipo="credito")
        matricula = Matricula.objects.filter(empresa=empresa,nombre_ciudad=request.user.ciudad)[0]
        tablas = ""
        tablas +="<table><thead><tr class='thead'><td>Moto</td>" \
             "<td>Precio Publico</td><td>Precio KIT</td></tr></thead><tbody>"
        for i in range(cotrows.count()):
            moto = cotrows[i].moto
            tablas+="<tr><td>"+moto.referencia+" "+moto.modelo+"</td><td>"+str(moto.precio_publico)+"</td><td>"+str(Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit())+"</td></tr>"
        tablas += "</tbody></table>"
        if cotrows_cont.count() > 0:
            tablas += "<table><thead><tr class='thead'><td>Moto</td>" \
             "<td>Total Moto</td></tr></thead><tbody>"
        for i in range(cotrows_cont.count()):
            moto = cotrows_cont[i].moto
            tablas+="<tr class='nothead'><td>"+moto.referencia+" "+moto.modelo+"</td>"
            total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit()+matricula.precio
            tablas+="<td>"+str(total_moto)+"</td></tr>"
        tablas+="</tbody></table>"
        for i in range(cotrows_credito.count()):
            n_cuotas = cotrows_credito[i].n_cuotas.count()
            moto = cotrows_credito[i].moto
            total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit(conprenda=True)+matricula.precio
            tablas += "<br><table><thead><tr class='thead'><td>Moto</td>"
            for j in range(n_cuotas):
                tablas+="<td>"+str(cotrows_credito[i].n_cuotas.all()[j].num_meses)+" cuotas</td>"
            tablas+="</tr></thead><tbody class='nothead'><tr><td>%s %s</td>"%(moto.referencia,moto.modelo)
            for j in range(n_cuotas):
                tablas+="<td>"+str(((total_moto-cotrows_credito[i].cuota_inicial)*(cotrows_credito[i].n_cuotas.all()[j].valor_por)))+"</td>"
            tablas+="</tr></tbody></table>"
        #html = render_to_string("cotizador/pdf_report.html",{'content':tablas,'cot':cot})
        requisitos = cot.requisitos.all()
        reqs = "<br>"
        for req in requisitos:
            s = registroRequisito.objects.filter(tabla = req)
            reqs+="<div class='reqs'>"
            reqs+="<table><thead><tr class='thead'><td>%s<td></tr></thead><tbody>"%req
            for i in s:
                reqs+="<tr><td>%s</td></tr>"%i.requisito
            reqs+="</tbody></table></div>"
        return PDFTemplateResponse(request,"cotizador/pdf_report.html",{'content':tablas,'cot':cot,'requisitos':reqs,})
        #return converter.render_to_pdf(html=html)
        #return HttpResponse(html)
    else:
        return HttpResponseRedirect("/cotizacion/")

def pdfamail(request,id_cot):
    cot = Cotizacion.objects.get(id=id_cot)
    empresa = request.session['enterprise']
    cotrows = CotizacionFila.objects.filter(cotizacion = cot.id)
    cotrows_cont = cotrows.filter(tipo="contado")
    cotrows_credito = cotrows.filter(tipo="credito")
    matricula = Matricula.objects.filter(empresa=empresa,nombre_ciudad=request.user.ciudad)[0]

    tablas ="<table><thead><tr class='thead'><td>Moto</td>" \
            "<td>Precio Publico</td><td>Precio KIT</td></tr></thead><tbody>"
    for i in range(cotrows.count()):
        moto = cotrows[i].moto
        tablas+="<tr><td>"+moto.referencia+" "+moto.modelo+"</td><td>"+str(moto.precio_publico)+"</td><td>"+str(Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit())+"</td></tr>"
    tablas +="</tbody></table><br>"
    if cotrows_cont.count() > 0:
        tablas += "<table><thead><tr class='thead'><td>Moto</td>" \
        "<td>Total Moto</td></tr></thead><tbody>"
    for i in range(cotrows_cont.count()):
       moto = cotrows_cont[i].moto
       tablas+="<tr class='nothead'><td>"+moto.referencia+" "+moto.modelo+"</td>"
       total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit()+matricula.precio
       tablas+="<td>"+str(total_moto)+"</td></tr>"
    tablas+="</tbody></table>"
    for i in range(cotrows_credito.count()):
       n_cuotas = cotrows_credito[i].n_cuotas.count()
       moto = cotrows_credito[i].moto
       total_moto = moto.precio_publico+Kit.objects.filter(empresa=empresa).filter(moto_asociada=moto)[0].totalkit(conprenda=True)+matricula.precio
       tablas += "<br><table><thead><tr class='thead'><td>Moto</td>"
       for j in range(n_cuotas):
          tablas+="<td>"+str(cotrows_credito[i].n_cuotas.all()[j].num_meses)+" cuotas</td>"
       tablas+="</tr></thead><tbody class='nothead'><tr><td>%s %s</td>"%(moto.referencia,moto.modelo)
       for j in range(n_cuotas):
          tablas+="<td>"+str(((total_moto-cotrows_credito[i].cuota_inicial)*(cotrows_credito[i].n_cuotas.all()[j].valor_por)))+"</td>"
       tablas+="</tr></tbody></table>"
    requisitos = cot.requisitos.all()
    reqs = "<br>"
    for req in requisitos:
        s = registroRequisito.objects.filter(tabla = req)
        reqs+="<div class='reqs'>"
        reqs+="<table><thead><tr class='thead'><td>%s<td></tr></thead><tbody>"%req
        for i in s:
            reqs+="<tr><td>%s</td></tr>"%i.requisito
        reqs+="</tbody></table></div>"
    pdf = PDFTemplateResponse(request,"cotizador/pdf_report.html",{'content':tablas,'cot':cot,'requisitos':reqs}).render()
    if pdf != None:
        email = cot.cliente.email
        empresa = request.session['enterprise']
        subject = 'Cotizacion en '+empresa.nombre+' '+str(date.today())
        body = unicode("\n"+"\n"+"Este mensaje fue autogenerado por el sistema. Por favor no contestar este mensaje\n"+ "Empresa : "+empresa.nombre+" Telefono: "+empresa.telefono+" Correo:"+empresa.correo+"\n"+"Direccion : "+empresa.direccion+"         \n"+"NIT: "+empresa.nit+"  Ciudad: "+empresa.ciudad+".")
        efrom = "sicobotero@hotmail.com"
        message = mail.EmailMessage(subject,body,efrom,to=[email,],headers = {'Reply-To': efrom})
        message.attach("Reporte.pdf",pdf.content,mimetype="application/pdf")
        message.send()
        return HttpResponseRedirect('/reporte/'+str(id_cot)+"/")
    else:
        return HttpResponse(status=404)

def get_imagen_moto(request,id_moto):
    moto = Moto.objects.get(id = id_moto)
    if not moto.imagen_preview.url == None:
        img = "<img src = '"+moto.imagen_preview.url+"' width='120px' />"
        return HttpResponse(content=img,content_type="text/html")


def get_cot_list(request):
    cotizaciones = Cotizacion.objects.filter(empresa = request.session.get('enterprise')).order_by("-id")
    return render_to_response("cotizador/lista_reportes_cotizaciones.html",{'cotizaciones':cotizaciones},context_instance=RequestContext(request))