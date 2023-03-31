from django.contrib import admin
from import_export import resources

from . import models

admin.site.register(models.MarkUp)


class VendaResource(resources.ModelResource):
    class Meta:
        model = models.Venda

class BasketItemResource(resources.ModelResource):
    class Meta:
        model = models.BasketItem
