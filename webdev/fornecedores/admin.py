from django.contrib import admin
from import_export import resources
from . import models


class FornecimentoResource(resources.ModelResource):
    class Meta:
        model = models.Fornecimento

class FornecedorResource(resources.ModelResource):
    class Meta:
        model = models.Fornecedor

class EmailResource(resources.ModelResource):
    class Meta:
        model = models.Email

class TelefoneResource(resources.ModelResource):
    class Meta:
        model = models.Telefone

class LocalResource(resources.ModelResource):
    class Meta:
        model = models.Local

class DadosBancariosResource(resources.ModelResource):
    class Meta:
        model = models.DadosBancarios

class DocumentoResource(resources.ModelResource):
    class Meta:
        model = models.Documento
