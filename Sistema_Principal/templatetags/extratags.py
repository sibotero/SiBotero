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

def is_in(value,args):
    for val in value:
        print type(val),type(args)
        if val == args:
            print "true"
            return True
    return False

def empty(value):
    if (len(value)==0 | value==None):
        return True
    return False

register.filter('get_count',get_count)
register.filter('concat',concat)
register.filter('lookup',lookup)
register.filter('len',get_length)
register.filter('is_in',is_in)
register.filter('empty',empty)

