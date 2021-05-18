from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    entrada = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'})
    )
    class Meta:
        model = Material
        fields = '__all__'
