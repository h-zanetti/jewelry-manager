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
    cpf = models.CharField('CPF', max_length=11, blank=True, null=True)
    birth_date = models.DateField(_('data de aniversário'), blank=True, null=True)
    observacao = models.TextField(_('observação'), blank=True, null=True)

    @classmethod
    def get_sortable_fields(cls):
        sortable_fields = [(f.name, f.verbose_name) for f in cls._meta.fields \
                            if f.name not in ['id', 'observacao']]
        return sortable_fields

    def get_nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    def __str__(self):
        return self.get_nome_completo()


class MarkUp(models.Model):
    key = models.CharField('nome', max_length=50)
    value = models.FloatField('valor')

    def __str__(self):
        return self.key


class Basket(models.Model):
    markup = models.ForeignKey(MarkUp, on_delete=models.SET_NULL, null=True, verbose_name="mark up")
    is_active = models.BooleanField(_('está ativo'), default=True)

    def get_items(self):
        return BasketItem.objects.filter(basket=self)
    
    def get_production_cost(self):
        cost = sum(item.get_production_cost() for item in self.get_items())
        return cost
    
    def get_sale_price(self):
        price = sum(item.get_sale_price() for item in self.get_items())
        return price


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name=_('carrinho de compras'))
    product = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, verbose_name=_('produto'))
    quantity = models.PositiveIntegerField(_('quantidade'), default=1)

    def get_production_cost(self):
        return self.quantity * self.product.get_custo_de_producao()

    def get_sale_price(self):
        price = float(self.get_production_cost())
        if self.basket.markup:
            price *= self.basket.markup.value
        return round(price, 2)


class Venda(models.Model):
    receita = OneToOneField(Receita, on_delete=models.CASCADE, null=True, blank=True, verbose_name="receita")
    basket = models.OneToOneField(Basket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="basket")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="cliente")
    data = models.DateField("data", default=timezone.now, null=True, blank=True)
    observacao = models.TextField('observação', blank=True, null=True)
    valor = models.DecimalField("valor", max_digits=8, decimal_places=2)
    PARCELAS_CHOICES = (
        (1, '1x'),(2, '2x'),(3, '3x'),
        (4, '4x'),(5, '5x'),(6, '6x'),
        (7, '7x'),(8, '8x'),(9, '9x'),
        (10, '10x'),(11, '11x'),(12, '12x'),
    )
    parcelas = models.IntegerField("parcelas", choices=PARCELAS_CHOICES, default=1)

    class Meta:
        get_latest_by = "data"

    @classmethod
    def get_sortable_fields(cls):
        sortable_fields = [(f.name, f.verbose_name) for f in cls._meta.fields \
                            if f.name not in ['id', 'cliente', 'produtos', 'observacao', 'receita']]
        return sortable_fields

    def __str__(self):
        return f'Venda #{self.id}'

    def get_sale_price(self):
        if self.value:
            return round(self.value, 2)
        price = self.basket.get_sale_price()
        if self.markup:
            price *= self.markup.value
        return round(price, 2)

    def get_installement_price(self):
        return round(self.get_sale_price() / self.parcelas, 2)

    def get_valor_parcela(self):
        return round(self.valor / self.parcelas, 2)

