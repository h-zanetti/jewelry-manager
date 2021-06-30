# from django.contrib import admin
from import_export import resources
from .models import Despesa

class DespesaResource(resources.ModelResource):
    class Meta:
        model = Despesa
        fields = ('id', 'data', 'categoria', 'valor', 'repetir', 'is_active', 'data_de_encerramento')