from django import forms
from .models import Fornecedor, Email, Telefone, Local, Fornecimento, DadosBancarios

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class EditarFornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ('foto', 'nome', 'documento')

class FornecimentoForm(forms.ModelForm):
    class Meta:
        model = Fornecimento
        fields = '__all__'

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = '__all__'

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = '__all__'


class DadosBancariosForm(forms.ModelForm):
    class Meta:
        model = DadosBancarios
        fields = '__all__'
