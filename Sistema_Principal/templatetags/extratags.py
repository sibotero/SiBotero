from django import template
from Sistema_Principal.models import Medio_Publicitario,Cotizacion
import SiCoBotero.settings
register = template.Library()

def concat(value,args):
    return str(value)+str(args)

def lookup(value,key):
    return value[key]

def get_length(value):
    return range(len(value))

def get_count(value):
    qset = Cotizacion.objects.filter(medio = value)
    conteo = qset.count()
    return conteo

def get_apps(value):
    apps = [app for app in SiCoBotero.settings.INSTALLED_APPS if not "django" in app]
    print apps
    return apps

register.filter('get_count',get_count)
register.filter('concat',concat)
register.filter('lookup',lookup)
register.filter('len',get_length)
register.filter('get_apps',get_apps)
