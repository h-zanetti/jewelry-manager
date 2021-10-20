from django import forms
from .models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from webdev.financeiro.models import Despesa

class MaterialForm(forms.ModelForm):
    foto = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    # altura = forms.DecimalField(
    #     widget=forms.widgets.NumberInput(
    #         attrs={'class': 'rounded-0 rounded-start'}
    #     ),
    #     required=False
    # )
    # largura = forms.DecimalField(
    #     widget=forms.widgets.NumberInput(
    #         attrs={'class': 'rounded-0'}
    #     ),
    #     required=False
    # )
    # comprimento = forms.DecimalField(
    #     widget=forms.widgets.NumberInput(
    #         attrs={'class': 'rounded-0 rounded-end'}
    #     ),
    #     required=False
    # )
    # peso = forms.DecimalField(
    #     widget=forms.widgets.NumberInput(
    #         attrs={'class': 'rounded-0 rounded-start'}
    #     ),
    #     required=False
    # )
    unidade_de_medida = forms.ChoiceField(
        choices=Material.UNIDADE_DE_MEDIDA_CHOICES,
        widget=forms.Select(
            attrs={'class': 'rounded-0 rounded-end'}
        ),
        required=False
    )
    observacao = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': "4",
                'style': "padding: 14px 10px",
            }
        ),
        required=False
    )
    class Meta:
        model = Material
        fields = '__all__'

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        exclude = ('despesa',)
