from django.db.models import Q
from django.contrib import messages
from django.http.response import HttpResponse
from tablib.core import Dataset
from webdev.produtos.admin import ProdutoResource
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Produto, MaterialDoProduto, Categoria, ServicoDoProduto
from .forms import ProdutoForm, MaterialDoProdutoForm, CategoriaForm
from webdev.produtos.forms import ServicoDoProdutoForm

@login_required
def categorias(request):
    CategoriaFormSet = modelformset_factory(Categoria, fields='__all__', can_delete=True, form=CategoriaForm)
    if request.method == 'POST':
        formset = CategoriaFormSet(request.POST)
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
        produto.pk = None

        if request.method == 'POST':
            form = ProdutoForm(request.POST, request.FILES)
            if form.is_valid():
                prod_duplicado = form.save()
                produto = Produto.objects.get(id=produto_id)
                # Duplicar materiais do produto
                for material_dp in produto.get_materiais():
                    mdp = MaterialDoProduto.objects.get(pk=material_dp.pk)
                    mdp.produto = prod_duplicado
                    mdp.pk = None
                    mdp.save()
                # Duplicar servicos do produto
                for servico_dp in produto.get_servicos():
                    sdp = ServicoDoProduto.objects.get(pk=servico_dp.pk)
                    sdp.produto = prod_duplicado
                    sdp.pk = None
                    sdp.save()
                return redirect('produtos:estoque_produtos')
        else:
            form = ProdutoForm(instance=produto)

        context = {
            'title': 'Duplicar Produto',
            'produto_id': produto_id,
            'form': form,
        }
        return render(request, 'produtos/duplicar_produto.html', context)
    except Produto.DoesNotExist:
        raise Http404('Produto não encontrado')

@login_required
def deletar_produto(request, produto_id):
    if request.method == 'POST':
        Produto.objects.get(id=produto_id).delete()
    return HttpResponseRedirect(reverse('produtos:estoque_produtos'))

@login_required
def estoque(request):
    if request.GET:
        produtos = Produto.objects.filter(
            Q(nome__icontains=request.GET.get('search')) |
            Q(colecao__icontains=request.GET.get('search')) |
            Q(familia__icontains=request.GET.get('search'))
        )
    else:
        produtos = Produto.objects.all()

    context = {
        'title': 'Estoque de Produtos',
        'import_url': reverse('produtos:importar_produtos'),
        'export_url': reverse('produtos:exportar_produtos'),
        'create_url': reverse('produtos:novo_produto'),
        'produtos': produtos,
    }
    return render(request, 'produtos/estoque_produtos.html', context)

@login_required
def adicionar_servico(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        if request.method == 'POST':
            form = ServicoDoProdutoForm(request.POST, initial={'produto': produto_id})
            if form.is_valid():
                form.save()
                messages.success(request, 'Serviço adicionado com sucesso.')
                next_url = request.POST.get('next')
                if 'submit-stay' in request.POST:
                    return redirect('produtos:adicionar_servico', produto_id)
                elif next_url:
                    return redirect(f'{next_url}')
                else:
                    return redirect('produtos:estoque_produtos')
        else:
            form = ServicoDoProdutoForm(initial={'produto': produto_id})

        context = {
            'title': f'Adicionar serviço ao produto {produto.nome} #{produto.id}',
            'produto': produto,
            'form': form,
        }
        return render(request, 'produtos/adicionar_servico.html', context)
    except:
        raise Http404('Produto não encontrado')

@login_required
def editar_servico_dp(request, servico_dp_id):
    try:
        servico_dp = ServicoDoProduto.objects.get(id=servico_dp_id)
        if request.method == 'POST':
            form = ServicoDoProdutoForm(request.POST, instance=servico_dp)
            if form.is_valid():
                form.save()
                messages.success(request, 'Serviço editado com sucesso.')
                return redirect('produtos:estoque_produtos')
        else:
            form = ServicoDoProdutoForm(instance=servico_dp)

        context = {
            'title': f'Editar serviço do produto',
            'servico_dp': servico_dp,
            'form': form
        }
        return render(request, 'produtos/editar_servico_dp.html', context)
    except:
        raise Http404('Serviço e produto não relacionados')

@login_required
def remover_servico_dp(request, servico_dp_id):
    if request.method == 'POST':
        ServicoDoProduto.objects.get(id=servico_dp_id).delete()
    return HttpResponseRedirect(reverse('produtos:estoque_produtos'))

@login_required
def adicionar_material(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except:
        raise Http404('Produto não encontrado')

    if request.method == 'POST':
        form = MaterialDoProdutoForm(request.POST)
        if form.is_valid():
            form.save()
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
        'produto': produto,
        'form': form,
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
        'material_dp': material_dp,
        'form': form
    }

    return render(request, 'produtos/editar_material_dp.html', context)

@login_required
def remover_material_dp(request, material_dp_id):
    if request.method == 'POST':
        MaterialDoProduto.objects.get(id=material_dp_id).delete()
    return HttpResponseRedirect(reverse('produtos:estoque_produtos'))

# Importação e exportação

@login_required
def exportar_produtos(request):
    dados = ProdutoResource().export()
    resposta = HttpResponse(dados.xls, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=produtos.xls'
    return resposta

@login_required
def importar_produtos(request):
    if request.method == 'POST':
        resource = ProdutoResource()
        dataset = Dataset()
        novos_produtos = request.FILES['myfile']
        dataset.load(novos_produtos.read(), 'xls')
        resource.import_data(dataset)
        return redirect('produtos:estoque_produtos')
        
    return render(request, 'base_form_file.html', {'title': "Importação de produtos"})

