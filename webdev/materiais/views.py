from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from webdev.materiais.models import Entrada, Material
from webdev.materiais.forms import EntradaForm, MaterialForm
from .admin import EntradaResource, MaterialResource
from tablib import Dataset

# Estoque
@login_required
def estoque_materiais(request):
    context = {
        'title': 'Estoque de matéria prima',
        'materiais': Material.objects.all()
    }
    return render(request, 'materiais/estoque_materiais.html', context)

@login_required
def cadastrar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('materiais:cadastrar_material')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('materiais:estoque_materiais')
    else:
        form = MaterialForm()

    context = {
        'title': 'Cadastrar matéria prima',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'materiais/material_form.html', context)

@login_required
def editar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
        if request.method == 'POST':
            form = MaterialForm(request.POST, request.FILES, instance=material)
            if form.is_valid():
                form.save()
                return redirect('materiais:estoque_materiais')
        else:
            form = MaterialForm(instance=material)

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
    resposta = HttpResponse(dados.xls, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=materiais.xls'
    return resposta

@login_required
def importar_materiais(request):
    if request.method == 'POST':
        resource = MaterialResource()
        dataset = Dataset()
        novos_materiais = request.FILES['myfile']
        dataset.load(novos_materiais.read(), 'xls')
        resource.import_data(dataset)
        return redirect('materiais:estoque_materiais')
        
    return render(request, 'base_form_file.html', {'title': "Importação de matérias primas"})

# Entradas
@login_required
def entradas_de_materiais(request):
    context = {
        'title': 'Entradas de matérias primas',
        'entradas': Entrada.objects.all()
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
        form = EntradaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            return redirect('materiais:entradas_de_materiais')
    else:
        form = EntradaForm(instance=entrada)

    context = {
        'title': 'Editar entrada de matéria prima',
        'form': form
    }

    return render(request, 'materiais/entrada_de_material.html', context)

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
    resposta = HttpResponse(dados.xls, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=entradas.xls'
    return resposta

@login_required
def importar_entradas(request):
    if request.method == 'POST':
        dataset = Dataset()
        novas_entradas = request.FILES['myfile']
        dataset.load(novas_entradas.read(), 'xls')
        # Validar dados
        is_valid = True
        for row in dataset:
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
            resource = EntradaResource()
            resource.import_data(dataset)
            return redirect('materiais:entradas_de_materiais')
        else:
            messages.error(request, error_msg)
            return redirect('materiais:importar_entradas')
        
    return render(request, 'base_form_file.html', {'title': "Importação de entradas de matérias primas"})
