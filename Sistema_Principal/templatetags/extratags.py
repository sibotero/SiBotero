from django import template

register = template.Library()

def concat(value,args):
    return str(value)+str(args)

register.filter('concat',concat)