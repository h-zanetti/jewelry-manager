from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import ProdutoForm

def estoque(request):
    return HttpResponse('Estoque de produtos')

def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProdutoForm()

    context = {
        'form': form
    }

    return render(request, 'produtos/novo_produto.html', context)