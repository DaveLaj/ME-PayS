from django import template

register = template.Library()

@register.filter
def neg(value):
    return -value