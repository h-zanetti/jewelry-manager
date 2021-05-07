from django import forms
from .models import Entrada, Material

class EntradaForm(forms.ModelForm):
    prefix = 'entrada'
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'})
    )
    class Meta:
        model = Entrada
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    prefix = 'material'
    class Meta:
        model = Material
        exclude = ['entrada']
