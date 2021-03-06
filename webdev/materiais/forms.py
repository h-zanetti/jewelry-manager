from django import forms
from .models import Entrada, Material
from django.core.exceptions import ValidationError

class CadastrarMaterialForm(forms.ModelForm):
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

    def clean_unidade_de_medida(self):
        unidade_de_medida = self.cleaned_data['unidade_de_medida']
        material = Material.objects.get(id=self.cleaned_data['material'].id)
        if material.unidade_de_medida and unidade_de_medida != material.unidade_de_medida:
            raise ValidationError('A unidade de medida de uma Entrada deve ser a mesma do Material em estoque.')
        return unidade_de_medida


class EditarEntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        exclude = ('despesa', 'alterar_estoque')

    def clean_unidade_de_medida(self):
        unidade_de_medida = self.cleaned_data['unidade_de_medida']
        material = Material.objects.get(id=self.cleaned_data['material'].id)
        if material.unidade_de_medida and unidade_de_medida != material.unidade_de_medida:
            raise ValidationError('A unidade de medida de uma Entrada deve ser a mesma do Material em estoque.')
        return unidade_de_medida

class MaterialActionForm(forms.Form):
    materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True, error_messages={'required': 'É necessário selecionar ao menos um material'}
    )
    action = forms.ChoiceField(choices=(('barcode', 'Gerar código de barras'),))

class SortMaterialsForm(forms.Form):
    field = forms.ChoiceField(choices=Material.get_sortable_fields(), label='Atributo')
    order = forms.ChoiceField(choices=(('', 'Crescente'), ('-', 'Decrescente')), required=False, label='Ordem')
