from import_export import resources
from .models import Entrada, Material
from django.contrib import admin

# admin.site.register(Material)
# admin.site.register(Entrada)

class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        exclude = ('foto', 'despesas')

class EntradaResource(resources.ModelResource):
    class Meta:
        model = Entrada
        exclude = ('despesa',)
