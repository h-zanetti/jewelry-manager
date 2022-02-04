from django import forms
from .models import Despesa, Receita

class CriarDespesaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'class': 'm-0'
        }),
    )
    data_de_encerramento = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'class': 'm-0'
        }),
    )
    repetir = forms.ChoiceField(
        choices=Despesa.REPETIR_CHOICES,
        required=False
    )
    class Meta:
        model = Despesa
        fields = '__all__'
        # exclude = ('is_active', 'data_de_encerramento')

class EditarDespesaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'class': 'm-0'
        }),
    )
    data_de_encerramento = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'class': 'm-0'
        }),
    )
    class Meta:
        model = Despesa
        fields = '__all__'

class ReceitaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'class': 'm-0'
        }),
    )
    class Meta:
        model = Receita
        fields = '__all__'

