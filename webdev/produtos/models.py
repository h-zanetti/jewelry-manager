from django.db import models
from django.utils.translation import gettext_lazy as _

class Categoria(models.Model):
    nome = models.CharField(_('Categoria'), max_length=150, unique=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    foto = models.ImageField(_('Foto do Produto'), upload_to='produtos', default='produtos/default.jpg', blank=True, null=True)
    nome = models.CharField(_('Nome'), max_length=150)
    colecao = models.CharField(_('Coleção'), max_length=150)
    familia = models.CharField(_('Família'), max_length=150, blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, verbose_name=_('Categorias'), blank=True)
    data_criacao = models.DateField(_('Data de Criação'), blank=True, null=True)
    unidades = models.IntegerField(_("Unidades em Estoque"), default=0)
    tamanho = models.IntegerField(_("Tamanho"), blank=True, null=True)

    def __str__(self):
        return self.nome
