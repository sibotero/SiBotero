from django import template
from Sistema_Principal.models import Medio_Publicitario,Cotizacion

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

register.filter('get_count',get_count)
register.filter('concat',concat)
register.filter('lookup',lookup)
register.filter('len',get_length)
