from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext_lazy as _
from webdev.produtos.models import Produto

class Cliente(models.Model):
    nome = models.CharField(_("Nome"), max_length=150)
    sobrenome = models.CharField(_("Sobrenome"), max_length=150)
    email = models.EmailField(_("Endereço de Email"), blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=15, blank=True, null=True)
    endereco = models.CharField(_('Endereço'), max_length=100, blank=True, null=True)

    def get_nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    def __str__(self):
        return self.get_nome_completo()

class Venda(models.Model):
    data = models.DateField(_("Data"))
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cliente"))
    produtos = models.ManyToManyField(Produto, verbose_name=_("Produtos"))
    PARCELAS_CHOICES = (
        (1, '1x'),
        (2, '2x'),
        (3, '3x'),
        (4, '4x'),
        (5, '5x'),
        (6, '6x'),
        (7, '7x'),
        (8, '8x'),
        (9, '9x'),
        (10, '10x'),
        (11, '11x'),
        (12, '12x'),
    )
    parcelas = models.IntegerField(_("Parcelas"), choices=PARCELAS_CHOICES, default=1)
    ultima_parcela = models.DateField(_("Última Parcela"), null=True, blank=True)
    total_pago = models.DecimalField(_("Total Pago"), max_digits=8, decimal_places=2)
    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return f'{self.cliente} - R${self.total_pago}'

    @property
    def categoria(self):
        return 'Venda'

    def get_preco_parcela(self):
        return round(self.total_pago / self.parcelas, 2)

    def get_parcela(self, data):
        parcela = self.parcelas - ((self.ultima_parcela.year - data.year) * 12 + (self.ultima_parcela.month - data.month))
        if parcela > 0 and parcela <= self.parcelas:
            return f"R$ {self.get_preco_parcela()} ({parcela}/{self.parcelas})"
        else:
            return None

    def get_todas_parcelas(self):
        parcelas = {}
        for i in range(0, self.parcelas):
            parcelas[self.data + relativedelta(months=i)] = self.get_preco_parcela()
        return parcelas

class Despesa(models.Model):
    data = models.DateField(_("Data"), default=timezone.now)
    categoria = models.CharField(_("Categoria"), max_length=150)
    total_pago = models.DecimalField(_("Valor"), max_digits=8, decimal_places=2)
    REPETIR_CHOICES = (
        ('n', 'Nunca'),
        ('m', 'Mensalmente'),
        ('a', 'Anualmente'),
    )
    repetir = models.CharField(_("Repetir"), max_length=1, choices=REPETIR_CHOICES)
    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return f'{self.data} {self.categoria}'

