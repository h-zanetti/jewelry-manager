from django import forms
from .models import Cliente, Venda
from webdev.financeiro.models import Receita
from webdev.produtos.models import Produto

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
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all().order_by('nome'), required=False)
    produtos = forms.ModelMultipleChoiceField(
        queryset=Produto.objects.all().order_by('nome'),
        widget=forms.SelectMultiple(
            attrs={'style': 'padding: 9px 6px 10px'}
        ),
        required=False
    )
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

