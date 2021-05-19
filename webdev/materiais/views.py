from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from import_export import resources
from webdev.materiais.models import Material
from webdev.materiais.forms import MaterialForm
from .admin import MaterialResource
from tablib import Dataset

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
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if next_url:
                return redirect(f"{next_url}")
            else:
                return redirect('materiais:estoque_materiais')
    else:
        form = MaterialForm()

    context = {
        'title': 'Entrada de matéria prima',
        'form': form,
    }

    return render(request, 'materiais/entrada_form.html', context)

@login_required
def editar_material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except:
        raise Http404('Material não encontrado')

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
    }

    return render(request, 'base_form_lg.html', context)

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
