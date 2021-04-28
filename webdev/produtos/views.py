from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ProdutoForm

def estoque(request):
    return HttpResponse('Estoque de produtos')

def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:estoque'))
        else:
            return render(request, 'produtos/novo_produto.html', {'form': form}, status=400)
    else:
        form = ProdutoForm()

    context = {
        'form': form
    }

    return render(request, 'produtos/novo_produto.html', context)