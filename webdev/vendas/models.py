from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from webdev.produtos.models import Produto
from webdev.financeiro.models import Receita

class Cliente(models.Model):
    nome = models.CharField(_("Nome"), max_length=150)
    sobrenome = models.CharField(_("Sobrenome"), max_length=150)
    email = models.EmailField(_("Email"), blank=True, null=True)
    telefone = models.CharField(_('Telefone'), max_length=15, blank=True, null=True)
    endereco = models.CharField(_('Endereço'), max_length=100, blank=True, null=True)

    def get_nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    def __str__(self):
        return self.get_nome_completo()

class Venda(models.Model):
    data = models.DateField(_("Data"), default=timezone.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cliente"))
    produtos = models.ManyToManyField(Produto, verbose_name=_("Produtos"))
    observacao = models.TextField(_('Observação'), blank=True, null=True)
    valor = models.DecimalField(_("Valor"), max_digits=8, decimal_places=2)
    receita = OneToOneField(Receita, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Receita"))
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

    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return f'Venda #{self.id}'
    
    # def get_receita(self):
    #     pass

    def get_valor_parcela(self):
        return round(self.valor / self.parcelas, 2)

    # def get_parcela(self, data):
    #     primeira_parcela = dt.date(self.data.year, self.data.month, 1)
    #     ultima_parcela = primeira_parcela + relativedelta(months=self.parcelas)
    #     pagamentos = 1 + relativedelta(ultima_parcela, dt.date(data.year, data.month, 1)).months
    #     parcela = self.parcelas - pagamentos
    #     if parcela > 0:
    #         # Formatando o float para o padrão brasileiro -> Ex: 12,000,000.00
    #         p_str = f"{self.get_valor_parcela():,.2f}".split('.')
    #         inteiro = '.'.join(p_str[0].split(','))
    #         parcela_str = f"{inteiro},{p_str[1]}"
    #         return f"R$ {parcela_str} ({parcela}/{self.parcelas})"
    #     else:
    #         return None
