from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from webdev.fornecedores.models import Fornecedor

class Entrada(models.Model):
    data = models.DateField(_("Data"), default=timezone.now , blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, verbose_name=_("Fornecedor"))
    unidades = models.IntegerField(_("Unidades Compradas"), default=1)
    total_pago = models.DecimalField(_("Total Pago"), max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.data} {self.fornecedor.nome}"

    def get_material(self):
        return Material.objects.filter(entrada=self).first()

class Material(models.Model):
    entrada = models.OneToOneField(Entrada, on_delete=models.CASCADE, null=True, verbose_name=_('Entrada'))
    foto = models.ImageField(_("Foto do Material"), upload_to='materiais', default='default.jpg', blank=True, null=True)
    nome = models.CharField(_("Material"), max_length=150)
    categoria = models.CharField(_("Categoria"), max_length=150)
    subcategoria = models.CharField(_("Subcategoria"), max_length=150, blank=True, null=True)
    qualidade = models.IntegerField(_("Qualidade"), default=0)
    altura = models.DecimalField(_("Altura"), max_digits=8, decimal_places=2, blank=True, null=True) 
    largura = models.DecimalField(_("Largura"), max_digits=8, decimal_places=2, blank=True, null=True) 
    comprimento = models.DecimalField(_("Comprimento"), max_digits=8, decimal_places=2, blank=True, null=True) 
    peso = models.DecimalField(_("Peso Unitário"), max_digits=8, decimal_places=2, blank=True, null=True) 
    UNIDADE_DE_MEDIDA_CHOICES = (
        ('g', 'Gramas'),
        ('ct', 'Quilates'),
    )
    unidade_de_medida = models.CharField(_("Unidade de Medida"), max_length=2, choices=UNIDADE_DE_MEDIDA_CHOICES, blank=True, null=True)
    unidades = models.IntegerField(_("Unidades em Estoque"), default=0)

    def __str__(self):
        return f"{self.nome} | {self.unidades} und. de {self.peso} {self.unidade_de_medida}"

    def get_dimenssoes(self):
        if self.altura and self.largura and self.comprimento:
            return f"{self.altura}x{self.largura}x{self.comprimento}"
        else:
            return "Indisponível"

    def get_peso(self):
        if self.peso and self.unidade_de_medida:
            return f"{self.peso} {self.unidade_de_medida}"
        else:
            return "Indisponível"
        