from tempfile import NamedTemporaryFile
from barcode import EAN13
from barcode.writer import ImageWriter
from django.core.files import File
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
    peso = models.DecimalField(_("peso total"), max_digits=8, decimal_places=2, default=0, blank=True)
    UNIDADE_DE_MEDIDA_CHOICES = (
        ('', 'Uniade de Medida'),
        ('g', 'Gramas'),
        ('ct', 'Quilates'),
    )
    unidade_de_medida = models.CharField(_("unidade de medida"), max_length=2, choices=UNIDADE_DE_MEDIDA_CHOICES, blank=True, null=True)
    estoque = models.IntegerField(_("unidades em estoque"), default=0, blank=True)
    observacao = models.TextField(_('observação'), blank=True, null=True)
    valor = models.DecimalField(_("valor"), max_digits=8, decimal_places=2, blank=True, default=0)
    barcode = models.ImageField(_('código de barras'), upload_to='materiais/barcode/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} #{self.id}"

    @classmethod
    def get_sortable_fields(cls):
        sortable_fields = [(f.name, f.verbose_name.title()) for f in cls._meta.fields \
                            if f.name not in ['id', 'foto', 'unidade_de_medida', 'observacao']]
        return sortable_fields

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
    
    def get_entradas(self):
        return Entrada.objects.filter(material=self)

    def get_ultima_entrada(self):
        entradas = self.get_entradas()
        if entradas:
            return entradas.latest()
        return 0

    def get_preco_unitario(self):
        entradas = self.get_entradas()
        if entradas:
            entrada = entradas.latest()
            return entrada.valor / entrada.unidades if entrada.unidades else 0
        else:
            return 0
    
    def get_preco_por_peso(self):
        entradas = self.get_entradas()
        if entradas:
            entrada = entradas.latest()
            return entrada.valor / entrada.peso if entrada.peso else 0
        else:
            return 0
    
    def get_opportunity_cost(self):
        if self.unidade_de_medida:
            return self.get_preco_por_peso() * self.peso
        return self.get_preco_unitario() * self.estoque

    def generate_barcode(self):
        img_temp_file = NamedTemporaryFile(delete=True)
        EAN13(format(self.id, '012'), writer=ImageWriter()).write(img_temp_file)
        temp_file = File(img_temp_file, name=f'{self.id}.png')
        if self.barcode:
            self.barcode.delete()
            self.save()
        self.barcode = temp_file
        self.save()
        return self.barcode
    
    def get_barcode(self):
        if self.barcode:
            return self.barcode
        else:
            return self.generate_barcode()


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
    alterar_estoque = models.BooleanField(_("alterar estoque"), default=True, help_text=_("Define se o peso e as unidades desta entrada devem ser adicionados ao estoque."))

    class Meta:
        get_latest_by ='data'

    def __str__(self):
        return f"{self.data} {self.material}"
