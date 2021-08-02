# from django.contrib import admin
from import_export import resources
from .models import Material

class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        exclude = ('foto', 'despesas')