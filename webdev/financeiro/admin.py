# from django.contrib import admin
from import_export import resources
from .models import Despesa

class DespesaResource(resources.ModelResource):
    class Meta:
        model = Despesa
        fields = '__all__'