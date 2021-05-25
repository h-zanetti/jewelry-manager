from django.forms import widgets
from webdev.fornecedores.models import Fornecedor
from django import forms
from .models import Material
from webdev.fornecedores.models import Fornecedor

class MaterialForm(forms.ModelForm):
    entrada = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
        required=False
    )
    foto = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.Select(
            attrs={'class': 'rounded-0 rounded-start'}
        )
    )
    altura = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-start'}
        ),
        required=False
    )
    largura = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0'}
        ),
        required=False
    )
    comprimento = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-end'}
        ),
        required=False
    )
    peso = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-start'}
        ),
        required=False
    )
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
