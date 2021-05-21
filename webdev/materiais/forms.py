from django.forms import widgets
from webdev.fornecedores.models import Fornecedor
from django import forms
from .models import Material
from webdev.fornecedores.models import Fornecedor

class MaterialForm(forms.ModelForm):
    entrada = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'})
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
        )
    )
    largura = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0'}
        )
    )
    comprimento = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-end'}
        )
    )
    peso = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-start'}
        )
    )
    unidade_de_medida = forms.ChoiceField(
        choices=Material.UNIDADE_DE_MEDIDA_CHOICES,
        widget=forms.Select(
            attrs={'class': 'rounded-0 rounded-end'}
        )
    )
    class Meta:
        model = Material
        fields = '__all__'
