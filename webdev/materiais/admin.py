from import_export import resources
from .models import Entrada, Material

class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        exclude = ('foto', 'despesas')

class EntradaResource(resources.ModelResource):
    class Meta:
        model = Entrada
        exclude = ('despesa')
