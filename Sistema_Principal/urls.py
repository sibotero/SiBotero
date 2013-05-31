# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import patterns,url
from Sistema_Principal.views import *


urlpatterns = patterns('Sistema_Principal.views',
    url(r'^login/',login,name = "login"),
    url(r'^cotizacion/',cotizacion,name="cotizacion"),
    url(r'^logout/',logout,name="logout"),
    url(r'^get_row/(?P<n_inline>.*)/$',get_row,name="get_row"),
    url(r'^agregar_cliente/',add_cliente,name="agregar_cliente"),
    url(r'^reporte/(?P<id_cot>.*)/$',report,name="reporte"),
    url(r'^reportepdf/(?P<id_cot>.*)/$',reportpdf,name="reportepdf"),
    url(r'^pdfacorreo/(?P<id_cot>.*)/$',pdfamail,name="reportepdfmail"),
    url(r'^getimagen/(?P<id_moto>.*)/$',get_imagen_moto,name="imagen_moto"),
    url(r'^historial_cotizaciones/$',get_cot_list,name="historial_cotizaciones"),
)
