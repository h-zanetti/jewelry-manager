from django.contrib import admin
from import_export import resources
from .models import Produto, Categoria

class ProdutoResource(resources.ModelResource):
    class Meta:
        model = Produto
        exclude = ('foto', 'servicos', 'materiais')

# admin.site.register(Categoria)