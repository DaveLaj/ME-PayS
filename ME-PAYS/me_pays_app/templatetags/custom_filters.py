from django import template

register = template.Library()

@register.filter
def neg(value):
    if value:
        return -value
    else:
        return 0
    

@register.filter
def none2zero(value):
    if value:
        return value
    else:
        return 0
    


@register.filter
def replace(value, args):
    old, new = args.split(',')
    return value.replace(old, new)