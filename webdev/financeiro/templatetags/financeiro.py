from django import template

register = template.Library()

@register.simple_tag
def get_parcela(venda, data):
    return venda.get_parcela(data)