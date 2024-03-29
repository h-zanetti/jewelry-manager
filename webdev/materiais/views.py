from tablib import Dataset
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Entrada, Material
from .forms import EditarEntradaForm, EntradaForm, CadastrarMaterialForm, MaterialActionForm, SortMaterialsForm
from .admin import EntradaResource, MaterialResource

# Estoque
@login_required
def estoque_materiais(request):
    if request.GET:
        # Filter
        if 'search' in request.GET:
            materiais = Material.objects.filter(
                Q(nome__icontains=request.GET.get('search')) |
                Q(categoria__icontains=request.GET.get('search')) |
                Q(subcategoria__icontains=request.GET.get('search'))
            )
        else:
            materiais = Material.objects.all()
        # Sort
        if 'sort-field' in request.GET:
            sort_form = SortMaterialsForm(request.GET, prefix='sort')
            if sort_form.is_valid():
                field = sort_form.data.get(sort_form.prefix + '-field')
                order = sort_form.data.get(sort_form.prefix + '-order')
                materiais = materiais.order_by(order + field)
        else:
            sort_form = SortMaterialsForm(prefix='sort')
    else:
        sort_form = SortMaterialsForm(prefix='sort')
        materiais = Material.objects.all()

    # Pagination
    paginator = Paginator(materiais, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'title': 'Estoque de matéria prima',
        'import_url': reverse('materiais:importar_materiais'),
        'export_url': reverse('materiais:exportar_materiais'),
        'create_url': reverse('materiais:cadastrar_material'),
        'actions_url': reverse('materiais:material_actions'),
        'materiais': page_obj,
        'sort_form': sort_form,
        'sorting': True if 'sort-field' in request.GET else False,
        'sort_by': f'sort-field={request.GET.get("sort-field")}&sort-order={request.GET.get("sort-order")}',
        'search_by': f"search={request.GET.get('search')}" if 'search' in request.GET else None,
    }
    return render(request, 'materiais/estoque_materiais.html', context)

@login_required
def cadastrar_material(request):
    if request.method == 'POST':
        form = CadastrarMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            messages.success(request, 'Material cadastrado com sucesso.')
            if form.cleaned_data.get('realizar_compra'):
                entrada_form = EntradaForm(request.POST, prefix='entrada')
                if entrada_form.is_valid():
                    entrada_form.save()
                    messages.success(request, 'Entrada efetuada com sucesso.')
            # Redirection
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('materiais:cadastrar_material')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('materiais:estoque_materiais')
    else:
        form = CadastrarMaterialForm()
        entrada_form = EntradaForm(prefix='entrada')

    context = {
        'title': 'Cadastrar matéria prima',
        'form': form,
        'entrada_form': entrada_form,
        'novo_obj': True
    }

    return render(request, 'materiais/material_form.html', context)

@login_required
def material_barcode(request):
    materials = Material.objects.all()
    if request.GET:
        params = request.GET.get('materials')
        params = params[1:-1].split(', ')
        materials = materials.filter(id__in=params)
    context = {
        'title': 'Códigos de Barras dos Materiais',
        'materials': materials
    }
    return render(request, 'materiais/material_barcode.html', context)

@login_required
def material_action_page(request):
    materials = Material.objects.all()
    if request.GET:
        form = MaterialActionForm(request.GET)
        if form.is_valid():
            action = form.cleaned_data.get('action')
            materials = form.cleaned_data.get('materials')
            materials = [m.id for m in materials]
            if action == 'barcode':
                base_url = reverse('materiais:material_barcode')
                query_string =  urlencode({'materials': materials})
                url = f'{base_url}?{query_string}'
                return redirect(url)

    else:
        form = MaterialActionForm()
    context = {
        'title': 'Ações em massa de materiais',
        'materials': materials,
        'form': form,
    }
    return render(request, 'materiais/material_actions.html', context)


@login_required
def editar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
        if request.method == 'POST':
            form = CadastrarMaterialForm(request.POST, request.FILES, instance=material)
            if form.is_valid():
                form.save()
                return redirect('materiais:estoque_materiais')
        else:
            form = CadastrarMaterialForm(instance=material)

        context = {
            'title': 'Editar matéria prima',
            'form': form,
            'material': material,
        }

    except:
        raise Http404('Material não encontrado')

    return render(request, 'materiais/editar_material.html', context)

@login_required
def deletar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except:
        raise Http404('Material não encontrado')

    if request.method == 'POST':
        material.delete()
    return HttpResponseRedirect(reverse('materiais:estoque_materiais'))

@login_required
def exportar_materiais(request):
    dados = MaterialResource().export()
    resposta = HttpResponse(dados.xlsx, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=materiais.xlsx'
    return resposta

@login_required
def importar_materiais(request):
    if request.method == 'POST':
        resource = MaterialResource()
        dataset = Dataset()
        novos_materiais = request.FILES['myfile']
        dataset.load(novos_materiais.read(), 'xlsx')
        resource.import_data(dataset)
        return redirect('materiais:estoque_materiais')
        
    return render(request, 'base_form_file.html', {'title': "Importação de matérias primas"})


# Entradas
@login_required
def entradas_de_materiais(request):
    entradas = Entrada.objects.all()
    if request.GET:
        # Filter
        if 'search' in request.GET:
            entradas = entradas.filter(
                Q(material__nome__icontains=request.GET.get('search')) |
                Q(fornecedor__nome__icontains=request.GET.get('search')) |
                Q(codigo_do_fornecedor__icontains=request.GET.get('search'))
            )

    # Pagination
    paginator = Paginator(entradas, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'title': 'Entradas de matérias primas',
        'import_url': reverse('materiais:importar_entradas'),
        'export_url': reverse('materiais:exportar_entradas'),
        'create_url': reverse('materiais:entrada_de_material'),
        'entradas': page_obj,
        # 'sort_form': sort_form,
        'sorting': True if 'sort-field' in request.GET else False,
        'sort_by': f'sort-field={request.GET.get("sort-field")}&sort-order={request.GET.get("sort-order")}',
        'search_by': f"search={request.GET.get('search')}" if 'search' in request.GET else None,
    }
    return render(request, 'materiais/entradas_de_materiais.html', context)

@login_required
def entrada_de_material(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            form.save()
            if 'submit-stay' in request.POST:
                return redirect('materiais:entrada_de_material')
            else:
                return redirect('materiais:estoque_materiais')
    else:
        form = EntradaForm()
    
    context = {
        'title': 'Entrada de material',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'materiais/entrada_form.html', context)

@login_required
def editar_entrada(request, entrada_id):
    try:
        entrada = Entrada.objects.get(id=entrada_id)
    except:
        raise Http404('Entrada não encontrada')

    if request.method == 'POST':
        form = EditarEntradaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            return redirect('materiais:entradas_de_materiais')
    else:
        form = EditarEntradaForm(instance=entrada)

    context = {
        'title': 'Editar entrada de matéria prima',
        'entrada': entrada,
        'form': form,
    }

    return render(request, 'materiais/editar_entrada.html', context)

@login_required
def deletar_entrada(request, entrada_id):
    try:
        entrada = Entrada.objects.get(id=entrada_id)
    except:
        raise Http404('Entrada não encontrada')

    if request.method == 'POST':
        entrada.delete()
    return HttpResponseRedirect(reverse('materiais:entradas_de_materiais'))


@login_required
def exportar_entradas(request):
    dados = EntradaResource().export()
    resposta = HttpResponse(dados.xlsx, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=entradas.xlsx'
    return resposta

@login_required
def importar_entradas(request):
    if request.method == 'POST':
        dataset = Dataset()
        novas_entradas = request.FILES['myfile']
        dataset.load(novas_entradas.read(), 'xlsx')
        # Validar dados
        is_valid = True
        for i, row in zip(range(len(dataset)), dataset):
            if not any(row):
                del dataset[i]
                continue
            material_id = int(row[2])
            try:
                material = Material.objects.get(id=material_id)
                if material.unidade_de_medida and material.unidade_de_medida != row[7]:
                    is_valid = False
                    error_msg = f'Unidade de medida inconsistente na entrada #{int(row[0])}'
                    break
            except Material.DoesNotExist:
                is_valid = False
                error_msg = f'Código de identificação #{material_id} inválido, nenhum material encontrado'
                break
        # Import data
        if is_valid:
            # resource = EntradaResource()
            # resource.import_data(dataset, raise_errors=True)
            # return redirect('materiais:entradas_de_materiais')
            try:
                resource = EntradaResource()
                resource.import_data(dataset, raise_errors=True)
                return redirect('materiais:entradas_de_materiais')
            except Exception as e:
                messages.error(request, e)
                return redirect('materiais:importar_entradas')
        else:
            messages.error(request, error_msg)
            return redirect('materiais:importar_entradas')
        
    return render(request, 'base_form_file.html', {'title': "Importação de entradas de matérias primas"})
