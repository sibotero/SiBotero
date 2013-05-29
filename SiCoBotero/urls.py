# -*- encoding: utf-8 -*-
import django
from django.conf.urls import patterns, include, url
from django.conf import settings
from Sistema_Principal import urls
from Sistema_Principal.views import *
import Sistema_Principal
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SiCoBotero.views.home', name='home'),
    # url(r'^SiCoBotero/', include('SiCoBotero.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$',RedirectView.as_view(url="login")),
    url(r'^admin/', include(admin.site.urls),name="admin"),
    url(r'^',include(Sistema_Principal.urls),name="cotizador"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)



