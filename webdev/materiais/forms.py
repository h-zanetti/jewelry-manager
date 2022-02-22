from django import forms
from .models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from webdev.financeiro.models import Despesa
from django.core.exceptions import ValidationError

class CadastrarMaterialForm(forms.ModelForm):
    foto = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    realizar_compra = forms.BooleanField(
        required=False,
        help_text="Cria também uma entrada e uma despesa."
    )

    class Meta:
        model = Material
        fields = '__all__'

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        exclude = ('despesa',)

    def clean_unidade_de_medida(self):
        unidade_de_medida = self.cleaned_data['unidade_de_medida']
        material = Material.objects.get(id=self.cleaned_data['material'].id)
        if material.unidade_de_medida and unidade_de_medida != material.unidade_de_medida:
            raise ValidationError('A unidade de medida de uma Entrada deve ser a mesma do Material em estoque.')
        return unidade_de_medida
