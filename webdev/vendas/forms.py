from django import forms

from webdev.financeiro.models import Receita
from webdev.produtos.models import Produto
from .models import Basket, BasketItem, Cliente, Venda

class ClienteForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
        required=False
    )
    class Meta:
        model = Cliente
        fields = '__all__'


class SortClientsForm(forms.Form):
    field = forms.ChoiceField(choices=Cliente.get_sortable_fields(), label='Atributo')
    order = forms.ChoiceField(choices=(('', 'Crescente'), ('-', 'Decrescente')), required=False, label='Ordem')


class VendaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
    )
    basket = forms.ModelChoiceField(
        queryset=Basket.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True,
        required=False
    )
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all().order_by('nome'), required=False)
    observacao = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': "4"}
        ),
        required=False
    )
    receita = forms.ModelChoiceField(
        queryset=Receita.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )
    class Meta:
        model = Venda
        fields = '__all__'


class SortSalesForm(forms.Form):
    field = forms.ChoiceField(choices=Venda.get_sortable_fields(), label='Atributo')
    order = forms.ChoiceField(choices=(('', 'Crescente'), ('-', 'Decrescente')), required=False, label='Ordem')


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        exclude = ('is_active',)


class BasketItemForm(forms.ModelForm):
    basket = forms.ModelChoiceField(
        queryset=Basket.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True, required=True
    )
    product = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.TextInput(),
        required=False
    )
    quantity = forms.IntegerField(required=False, min_value=1, initial=1)

    class Meta:
        model = BasketItem
        fields = '__all__'
