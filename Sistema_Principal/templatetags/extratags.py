from django import template

register = template.Library()

def concat(value,args):
    return str(value)+str(args)

def lookup(value,key):
    return value[key]

def get_length(value):
    return range(len(value))

register.filter('concat',concat)
register.filter('lookup',lookup)
register.filter('len',get_length)
