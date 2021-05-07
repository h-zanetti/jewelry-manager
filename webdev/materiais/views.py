from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from webdev.materiais.models import Entrada, Material
from webdev.materiais.forms import EntradaForm, MaterialForm

@login_required
def entradas(request):
    context = {
        'title': 'Lista de entradas',
        'entradas': Entrada.objects.all()
    }
    return render(request, 'materiais/entradas.html', context)

@login_required
def estoque_materiais(request):
    context = {
        'title': 'Estoque de matéria prima',
        'materiais': Material.objects.all()
    }
    return render(request, 'materiais/estoque_materiais.html', context)

@login_required
def nova_entrada(request):
    if request.method == 'POST':
        entrada_form = EntradaForm(request.POST, prefix='entrada')
        material_form = MaterialForm(request.POST, prefix='material')
        if entrada_form.is_valid() and material_form.is_valid():
            entrada = entrada_form.save()
            material = material_form.save(commit=False)
            material.entrada = entrada
            material.save()
            next_url = request.POST.get('next')
            if next_url:
                return redirect(f"{next_url}")
            else:
                return redirect('materiais:estoque_materiais')
    else:
        entrada_form = EntradaForm(prefix='entrada')
        material_form = MaterialForm(prefix='material')

    context = {
        'title': 'Adicionar novo fornecedor',
        'entrada_form': entrada_form,
        'material_form': material_form
    }

    return render(request, 'materiais/entrada_form.html', context)

@login_required
def editar_entrada(request, entrada_id, material_id):
    try:
        entrada = Entrada.objects.get(id=entrada_id)
        material = Material.objects.get(id=material_id)
    except:
        raise Http404('Entrada ou material não encontrados')

    if request.method == 'POST':
        entrada_form = EntradaForm(request.POST, prefix='entrada', instance=entrada)
        material_form = MaterialForm(request.POST, prefix='material', instance=material)
        if entrada_form.is_valid() and material_form.is_valid():
            entrada_form.save()
            material_form.save()
            next_url = request.POST.get('next')
            if next_url:
                return redirect(f"{next_url}")
            else:
                return redirect('materiais:estoque_materiais')
    else:
        entrada_form = EntradaForm(prefix='entrada', instance=entrada)
        material_form = MaterialForm(prefix='material', instance=material)

    context = {
        'title': 'Editar entrada de matéria prima',
        'entrada_form': entrada_form,
        'material_form': material_form
    }

    return render(request, 'materiais/entrada_form.html', context)

@login_required
def deletar_entrada(request, entrada_id):
    if request.method == 'POST':
        Entrada.objects.get(id=entrada_id).delete()
    return HttpResponseRedirect(reverse('materiais:entradas'))

@login_required
def editar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except:
        raise Http404('Material não encontrado')

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materiais:estoque_materiais')
    else:
        form = MaterialForm(instance=material)

    context = {
        'title': 'Editar matéria prima',
        'form': form,
    }

    return render(request, 'base_form_lg.html', context)

@login_required
def deletar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except:
        raise Http404('Material não encontrado')

    if request.method == 'POST':
        if request.POST.get('deletar_entrada'):
            material.entrada.delete()
        material.delete()
    return HttpResponseRedirect(reverse('materiais:estoque_materiais'))
