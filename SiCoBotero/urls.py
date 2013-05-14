import django
from django.conf.urls import patterns, include, url
from django.conf import settings
from Sistema_Principal.views import *
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
    url(r'^login/',login,name = "login"),
    url(r'^cotizacion/',cotizacion,name="cotizacion"),
    url(r'^logout/',logout,name="logout"),
    url(r'^add_cliente/',add_cliente,name="add_cliente"),
    url(r'^thanks/',gracias,name="gracias"),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)



