from webdev.financeiro.models import Despesa
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from webdev.fornecedores.models import Fornecedor

class Material(models.Model):
    foto = models.ImageField(_("foto do material"), upload_to='materiais', default='default.jpg', blank=True)
    nome = models.CharField(_("nome do material"), max_length=150)
    categoria = models.CharField(_("categoria"), max_length=150)
    subcategoria = models.CharField(_("subcategoria"), max_length=150, blank=True, null=True)
    qualidade = models.IntegerField(_("qualidade"), default=1, blank=True)
    altura = models.DecimalField(_("altura"), max_digits=8, decimal_places=2, blank=True, null=True)
    largura = models.DecimalField(_("largura"), max_digits=8, decimal_places=2, blank=True, null=True)
    comprimento = models.DecimalField(_("comprimento"), max_digits=8, decimal_places=2, blank=True, null=True)
    peso = models.DecimalField(_("peso total"), max_digits=8, decimal_places=2, blank=True, null=True)
    UNIDADE_DE_MEDIDA_CHOICES = (
        ('', 'Uniade de Medida'),
        ('g', 'Gramas'),
        ('ct', 'Quilates'),
        ('cm', 'Centímetros'),
    )
    unidade_de_medida = models.CharField(_("unidade de medida"), max_length=2, choices=UNIDADE_DE_MEDIDA_CHOICES, blank=True, null=True)
    estoque = models.IntegerField(_("unidades em estoque"), default=0, blank=True)
    observacao = models.TextField(_('observação'), blank=True, null=True)

    def __str__(self):
        return f"{self.nome} #{self.id}"

    def get_dimensoes(self):
        dimensoes = [self.altura, self.largura, self.comprimento]
        has_dimensoes = True if self.largura and self.comprimento else False
        if has_dimensoes:
            if dimensoes[0]:
                return f"{dimensoes[0]} x {dimensoes[1]} x {dimensoes[2]}"
            else:
                return f"{dimensoes[1]} x {dimensoes[2]}"
        else:
            return "Indisponível"

    def get_peso(self):
        if self.peso and self.unidade_de_medida:
            return f"{self.peso} {self.unidade_de_medida}"
        else:
            return "Indisponível"
    
    def get_preco_unitario(self):
        entradas = Entrada.objects.filter(material=self)
        if entradas:
            entrada = entradas.latest()
            valor_unitario = entrada.valor / entrada.unidades
            return valor_unitario
        else:
            return 0
    
    def get_preco_por_peso(self):
        entrada = Entrada.objects.filter(material=self)
        if entrada:
            entrada = entrada.latest()
            if entrada.peso:
                valor_peso = entrada.valor / entrada.peso
                return valor_peso
            else:
                return entrada.valor
        else:
            return 0
    
    def get_opportunity_cost(self):
        return self.get_preco_unitario() * self.estoque

    def get_entradas(self):
        return Entrada.objects.filter(material=self)


class Entrada(models.Model):
    data = models.DateField(_("data"), default=timezone.now)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name=_("material"))
    despesa = models.OneToOneField(Despesa, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("despesa"))
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("fornecedor"))
    codigo_do_fornecedor = models.CharField(_("código do fornecedor"), max_length=50, null=True, blank=True, help_text="Código utilizado pelo fornecedor para identificar este produto.")
    unidades = models.IntegerField(_("unidades compradas"), default=1)
    peso = models.DecimalField(_("peso total"), max_digits=8, decimal_places=2, blank=True, null=True) 
    UNIDADE_DE_MEDIDA_CHOICES = (
        ('', 'Uniade de Medida'),
        ('g', 'Gramas'),
        ('ct', 'Quilates'),
    )
    unidade_de_medida = models.CharField(_("unidade de medida"), max_length=2, choices=UNIDADE_DE_MEDIDA_CHOICES, blank=True, null=True)
    valor = models.DecimalField(_("valor total"), max_digits=8, decimal_places=2)

    class Meta:
        get_latest_by ='data'

    def __str__(self):
        return f"{self.data} {self.material}"
