from django.db import models
from django.utils.translation import gettext_lazy as _
from webdev.fornecedores.models import Servico
from webdev.materiais.models import Material

class Categoria(models.Model):
    nome = models.CharField(_('Categoria'), max_length=150, unique=True)

    def __str__(self):
        return self.nome

class MaterialDoProduto(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name=_("Material"))
    unidades = models.IntegerField(_("Unidades Utilizadas"), default=1)
    peso = models.DecimalField(_("Peso Unitário"), max_digits=8, decimal_places=2, blank=True, null=True) 
    UNIDADE_DE_MEDIDA_CHOICES = (
        ('g', 'Gramas'),
        ('ct', 'Quilates'),
    )
    unidade_de_medida = models.CharField(_("Unidade de Medida"), max_length=2, choices=UNIDADE_DE_MEDIDA_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.material.nome} {self.unidades} unid."
    
    def get_peso(self):
        if self.peso and self.unidade_de_medida:
            return f"{self.peso} {self.unidade_de_medida}"
        else:
            return self.material.get_peso()

    def get_custo(self):
        preco = 0
        if self.peso:
            preco = self.peso * self.material.get_preco_por_peso()
        else:
            preco= self.unidades * self.material.get_preco_unitario()
        return preco

class Produto(models.Model):
    foto = models.ImageField(_('Foto do Produto'), upload_to='produtos', default='default.jpg', blank=True, null=True)
    nome = models.CharField(_('Nome'), max_length=150)
    colecao = models.CharField(_('Coleção'), max_length=150)
    familia = models.CharField(_('Família'), max_length=150, blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, verbose_name=_('Categorias'), blank=True)
    data_criacao = models.DateField(_('Data de Criação'), blank=True, null=True)
    unidades = models.IntegerField(_("Unidades em Estoque"), default=0)
    tamanho = models.IntegerField(_("Tamanho"), blank=True, null=True)
    servicos = models.ManyToManyField(Servico, verbose_name=_("Serviços"), blank=True)
    materiais = models.ManyToManyField(MaterialDoProduto, verbose_name=_("Materiais"), blank=True)

    def __str__(self):
        return f"{self.nome}"

    def get_custo_de_producao(self):
        custo = 0
        for servico in self.servicos.all():
            custo += servico.total_pago
        for material_dp in self.materiais.all():
            custo += material_dp.get_custo()
        return round(custo, 2)
                