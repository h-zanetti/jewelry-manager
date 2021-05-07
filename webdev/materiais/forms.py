from django import forms
from .models import Entrada, Material

class EntradaForm(forms.ModelForm):
    prefix = 'entrada'
    class Meta:
        model = Entrada
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    prefix = 'material'
    class Meta:
        model = Material
        exclude = ['entrada']
