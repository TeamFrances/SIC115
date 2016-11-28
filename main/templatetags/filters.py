#coding: utf-8

from django.template.defaultfilters import register


@register.filter(name='porcentformat')
def porcentformat(val):
    try:
        val = val * 100
        return str(val) + "%"
    except:
        return val