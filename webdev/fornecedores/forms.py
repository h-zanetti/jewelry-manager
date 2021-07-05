from django import forms
from django.forms import widgets
from .models import Fornecedor, Email, Telefone, Local, Fornecimento, DadosBancarios, Servico, Documento

class FornecedorForm(forms.ModelForm):
    fornecimento = forms.ModelMultipleChoiceField(
        queryset=Fornecimento.objects.all().order_by('nome').order_by('qualidade'),
        widget=forms.SelectMultiple(
            attrs={'class': 'rounded-0 rounded-start'}
        )
    )
    class Meta:
        model = Fornecedor
        fields = ('nome', 'fornecimento')

class FornecimentoForm(forms.ModelForm):
    class Meta:
        model = Fornecimento
        fields = '__all__'

class EmailForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.HiddenInput()
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Novo Email"}
        )
    )
    class Meta:
        model = Email
        fields = '__all__'

class TelefoneForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Telefone
        fields = '__all__'

class LocalForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Local
        fields = '__all__'

class DadosBancariosForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.HiddenInput()
    )
    tipo_de_transacao = forms.ChoiceField(
        choices=DadosBancarios.TIPO_DE_TRANSACAO_CHOICES,
    )
    class Meta:
        model = DadosBancarios
        fields = '__all__'

class DocumentoForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Documento
        fields = '__all__'

class ServicoForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'})
    )
    class Meta:
        model = Servico
        exclude = ('despesa',)
