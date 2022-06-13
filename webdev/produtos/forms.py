from faulthandler import disable
from django import forms
from .models import Produto, Categoria, MaterialDoProduto, ServicoDoProduto

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
        exclude = ('servicos', 'materiais', 'barcode')


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
    

class ServicoDoProdutoForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        disabled=True
    )
    class Meta:
        model = ServicoDoProduto
        fields = '__all__'


class ProductActionForm(forms.Form):
    produtos = forms.ModelMultipleChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True, error_messages={'required': 'É necessário selecionar ao menos um produto'}
    )
    action = forms.ChoiceField(choices=(('barcode', 'Gerar código de barras'),))


class SortProductsForm(forms.Form):
    field = forms.ChoiceField(choices=Produto.get_sortable_fields(), label='Atributo')
    order = forms.ChoiceField(choices=(('', 'Crescente'), ('-', 'Decrescente')), required=False, label='Ordem')
