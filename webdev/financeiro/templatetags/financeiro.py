from django import template

register = template.Library()

@register.simple_tag
def get_parcela(parcela, data):
    if parcela.get_parcela_atual(data):
        return parcela.get_parcela_atual(data)