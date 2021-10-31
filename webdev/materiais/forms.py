from django import forms
from .models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from webdev.financeiro.models import Despesa

class MaterialForm(forms.ModelForm):
    foto = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )

    class Meta:
        model = Material
        fields = '__all__'

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        exclude = ('despesa',)
