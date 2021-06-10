from django import forms
from .models import Cliente, Venda
from webdev.financeiro.models import Receita
from webdev.produtos.models import Produto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class VendaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
    )
    produtos = forms.ModelMultipleChoiceField(
        queryset=Produto.objects.all(),
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
