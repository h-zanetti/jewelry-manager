from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Produto, MaterialDoProduto, Categoria
from .forms import ProdutoForm, MaterialDoProdutoForm, CategoriaForm
from webdev.fornecedores.forms import ServicoForm

@login_required
def categorias(request):
    CategoriaFormSet = modelformset_factory(Categoria, fields='__all__', can_delete=True, form=CategoriaForm)
    if request.method == 'POST':
        formset = CategoriaFormSet(request.POST, error_messages={
            'nome': 'Categoria com este nome já existe.'
        })
        if formset.is_valid():
            formset.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('produtos:categorias')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('produtos:estoque_produtos')
    else:
        formset = CategoriaFormSet()

    context = {
        'title': 'Categorias de Produtos Disponíveis',
        'formset': formset
    }

    return render(request, 'produtos/categorias.html', context)

@login_required
def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('produtos:novo_produto')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('produtos:estoque_produtos')
    else:
        form = ProdutoForm()

    context = {
        'title': 'Adicionar Novo Produto',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'produtos/novo_produto.html', context)

@login_required
def editar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except:
        raise Http404('Produto não encontrado')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:estoque_produtos')
    else:
        form = ProdutoForm(instance=produto)

    context = {
        'title': 'Editar Produto',
        'form': form,
        'novo_obj': False
    }

    return render(request, 'produtos/editar_produto.html', context)

@login_required
def duplicar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        initial = produto.__dict__
        initial.pop('_state')
        initial.pop('id')
    except:
        raise Http404('Produto não encontrado')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            novo_produto = form.save()
            if 'submit-stay' in request.POST:
                return redirect(reverse('produtos:duplicar_produto', kwargs={'produto_id': novo_produto.id}))
            else:
                return redirect('produtos:estoque_produtos')
    else:
        form = ProdutoForm(initial=initial)

    context = {
        'title': 'Duplicar Produto',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'produtos/novo_produto.html', context)

@login_required
def deletar_produto(request, produto_id):
    if request.method == 'POST':
        Produto.objects.get(id=produto_id).delete()
    return HttpResponseRedirect(reverse('produtos:estoque_produtos'))

@login_required
def estoque(request):
    context = {
        'title': 'Estoque de Produtos',
        'produtos': Produto.objects.all()
    }
    return render(request, 'produtos/estoque_produtos.html', context)

@login_required
def adicionar_servico(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except:
        raise Http404('Produto não encontrado')

    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save()
            produto.servicos.add(servico)
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('produtos:adicionar_servico', produto_id)
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('produtos:estoque_produtos')
    else:
        form = ServicoForm()

    context = {
        'title': f'Adicionar serviço ao produto {produto.nome} #{produto.id}',
        'form': form
    }

    return render(request, 'fornecedores/servico_form.html', context)

@login_required
def adicionar_material(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except:
        raise Http404('Produto não encontrado')

    if request.method == 'POST':
        form = MaterialDoProdutoForm(request.POST)
        if form.is_valid():
            material_dp = form.save()
            if not material_dp.peso:
                material_dp.peso = material_dp.material.peso
                material_dp.unidade_de_medida = material_dp.material.unidade_de_medida
                material_dp.save()
            produto.materiais.add(material_dp)
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('produtos:adicionar_material', produto_id)
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('produtos:estoque_produtos')
    else:
        form = MaterialDoProdutoForm()

    context = {
        'title': f'Adicionar material ao produto {produto.nome} #{produto.id}',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'produtos/adicionar_material.html', context)

@login_required
def editar_material_dp(request, material_dp_id):
    try:
        material_dp = MaterialDoProduto.objects.get(id=material_dp_id)
    except:
        raise Http404('Material e produto não relacionados')

    if request.method == 'POST':
        form = MaterialDoProdutoForm(request.POST, instance=material_dp)
        if form.is_valid():
            material_dp = form.save()
            return redirect('produtos:estoque_produtos')
    else:
        form = MaterialDoProdutoForm(instance=material_dp)

    context = {
        'title': f'Editar material do produto',
        'form': form
    }

    return render(request, 'produtos/adicionar_material.html', context)

@login_required
def remover_material_dp(request, material_dp_id):
    if request.method == 'POST':
        MaterialDoProduto.objects.get(id=material_dp_id).delete()
    return HttpResponseRedirect(reverse('produtos:estoque_produtos'))
