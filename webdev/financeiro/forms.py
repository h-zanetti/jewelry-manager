from django.utils import timezone
from django import forms
from .models import Despesa, Cliente, Venda

class DespesaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'class': 'm-0'}),
    )
    repetir = forms.ChoiceField(
        choices=Despesa.REPETIR_CHOICES,
        initial='n'
    )
    class Meta:
        model = Despesa
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class VendaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
    )
    class Meta:
        model = Venda
        exclude = ('ultima_parcela',)
