from django import forms
from .models import Produto, Categoria, MaterialDoProduto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        error_messages = {
            'nome': {
                'unique': 'Categoria com este nome já existe.',
            }
        }

class ProdutoForm(forms.ModelForm):
    foto = forms.ImageField(
        widget=forms.FileInput(),
        required=False
    )
    data_criacao = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}),
        required=False
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'rows': "5",
                'style': 'padding: 9px 6px;'
            }
        ),
        help_text='Precione "Ctrl", ou "Command", para selecionar múltiplas opções ou remover alguma seleção.',
        required=False
    )
    observacao = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': "4"}
        ),
        required=False
    )
    class Meta:
        model = Produto
        exclude = ('servicos', 'materiais')

class MaterialDoProdutoForm(forms.ModelForm):
    peso = forms.IntegerField(
        widget=forms.widgets.NumberInput(
            attrs={'class': 'rounded-0 rounded-start'}
        ),
        required=False
    )
    unidade_de_medida = forms.ChoiceField(
        choices=MaterialDoProduto.UNIDADE_DE_MEDIDA_CHOICES,
        widget=forms.Select(
            attrs={'class': 'rounded-0 rounded-end'}
        ),
        required=False
    )
    class Meta:
        model = MaterialDoProduto
        fields = '__all__'