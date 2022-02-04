from django import template

register = template.Library()

@register.simple_tag
def get_parcela(transaction, data):
    if transaction.get_parcela(data):
        return transaction.get_parcela(data)