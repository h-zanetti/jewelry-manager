from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm
from django.contrib.auth.decorators import login_required

@login_required
def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:estoque')
    else:
        form = ProdutoForm()

    context = {
        'title': 'Adicionar Novo Produto',
        'form': form
    }

    return render(request, 'base_form_lg.html', context)

@login_required
def estoque(request):
    context = {
        'title': 'Estoque de Produtos',
        'produtos': Produto.objects.all()
    }
    return render(request, 'produtos/estoque_produtos.html', context)