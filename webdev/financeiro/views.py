from django.http.response import HttpResponse
from tablib.core import Dataset
from .admin import DespesaResource
from calendar import monthrange
import datetime as dt
from itertools import chain
from django.db.models.aggregates import Sum
from django.db.models.functions.datetime import TruncMonth
from django.db.models.query_utils import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from .models import Despesa, Parcela, Receita
from .forms import CriarDespesaForm, EditarDespesaForm, ReceitaForm

# Receitas
@permission_required('financeiro.view_receita', raise_exception=True)
def receitas(request):
    context = {
        'title': 'Minhas receitas',
        'receitas': Receita.objects.all()
    }
    return render(request, 'financeiro/receitas.html', context)

@permission_required('financeiro.add_receita', raise_exception=True)
def nova_receita(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('financeiro:nova_receita')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('financeiro:receitas')
    else:
        form = ReceitaForm()

    context = {
        'title': 'Nova receita',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'financeiro/form_receita.html', context)

@permission_required('financeiro.change_receita', raise_exception=True)
def editar_receita(request, receita_id):
    try:
        receita = Receita.objects.get(id=receita_id)
    except:
        raise Http404("Despesa não encontrada")

    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('financeiro:receitas')
    else:
        form = ReceitaForm(instance=receita)

    context = {
        'title': 'Editar receita',
        'form': form,
    }

    return render(request, 'financeiro/form_receita.html', context)

@permission_required('financeiro.delete_receita', raise_exception=True)
def deletar_receita(request, receita_id):
    if request.method == 'POST':
        Receita.objects.get(id=receita_id).delete()
    return HttpResponseRedirect(reverse('financeiro:receitas'))

# Despesas
@permission_required('financeiro.view_despesa', raise_exception=True)
def despesas(request):
    context = {
        'title': 'Minhas despesas',
        'despesas': Despesa.objects.all()
    }
    return render(request, 'financeiro/despesas.html', context)

@permission_required('financeiro.add_despesa', raise_exception=True)
def nova_despesa(request):
    if request.method == 'POST':
        form = CriarDespesaForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('financeiro:nova_despesa')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('financeiro:despesas')
    else:
        form = CriarDespesaForm()

    context = {
        'title': 'Nova despesa',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'financeiro/form_despesa.html', context)

@permission_required('financeiro.change_despesa', raise_exception=True)
def editar_despesa(request, despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id)
    except:
        raise Http404("Despesa não encontrada")

    if request.method == 'POST':
        form = EditarDespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            # despesa_edt = form.save()
            # if despesa_edt.encerrada and not despesa_edt.data_de_encerramento:
            #     despesa_edt.data_de_encerramento = timezone.localdate()
            # despesa_edt.save()
            return redirect('financeiro:despesas')
    else:
        form = EditarDespesaForm(instance=despesa)

    context = {
        'title': 'Editar despesa',
        'form': form,
    }

    return render(request, 'financeiro/form_despesa.html', context)

@permission_required('financeiro.delete_despesa', raise_exception=True)
def deletar_despesa(request, despesa_id):
    if request.method == 'POST':
        Despesa.objects.get(id=despesa_id).delete()
    return HttpResponseRedirect(reverse('financeiro:despesas'))

@permission_required('financeiro.view_despesa', raise_exception=True)
def exportar_despesas(request):
    dados = DespesaResource().export()
    resposta = HttpResponse(dados.xls, content_type='application/vnd.ms-excel')
    resposta['Content-Disposition'] = 'attachment; filename=despesas.xls'
    return resposta

@permission_required('financeiro.add_despesa', raise_exception=True)
def importar_despesas(request):
    if request.method == 'POST':
        resource = DespesaResource()
        dataset = Dataset()
        novas_despesas = request.FILES['myfile']
        dataset.load(novas_despesas.read(), 'xls')
        resource.import_data(dataset)
        return redirect('financeiro:despesas')
        
    return render(request, 'base_form_file.html', {'title': "Importação de despesas"})

# Fluxo de Caixa
@permission_required('financeiro.view_despesa', raise_exception=True)
@permission_required('financeiro.view_receita', raise_exception=True)
def fluxo_de_caixa(request, ano, mes):
    # Dados do gráfico - Fluxo de caixa anual
    dados = [0 for i in range(12)]
    receitas = Parcela.objects.filter(data__year=ano).annotate(
        mes=TruncMonth('data')).values('mes').annotate(valor=Sum('valor'))
    for receita in receitas:
        index = receita['mes'].month - 1
        dados[index] += float(receita['valor'])
    despesas_variaveis = Despesa.objects.filter(repetir='', data__year=ano)
    despesas_mensais = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__year__gte=ano),
        repetir='m', data__year__lte=ano)
    despesas_anuais = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__year__gte=ano),
        repetir='a', data__year__lte=ano)
    despesas = [despesas_anuais, despesas_mensais, despesas_variaveis]
    for qs in despesas:
        for despesa in qs:
            index = despesa.data.month - 1
            if despesa.repetir == 'm':
                if despesa.data.year < ano:
                    for i in range(12):
                        dados[i] -= float(despesa.valor)
                else:
                    for i in range(index, 12):
                        dados[i] -= float(despesa.valor)
            else:
                dados[index] -= float(despesa.valor)

    # Dados da tabela - Fluxo de caixa mensal
    parcelas = Parcela.objects.filter(data__year=ano, data__month=mes)
    despesas_variaveis = Despesa.objects.filter(repetir='', data__year=ano, data__month=mes)
    despesas_mensais = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__gte=f'{ano}-{mes}-01'),
        repetir='m', data__lte=f'{ano}-{mes}-{monthrange(ano, mes)[1]}')
    despesas_anuais = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__gte=f'{ano}-{mes}-01'),
        repetir='a', data__month=mes, data__year__lte=ano)
    transacoes = sorted(
        chain(parcelas, despesas_variaveis, despesas_mensais, despesas_anuais),
        key=lambda instance: instance.data
    )

    context = {
        # Data da requisição
        'data': dt.date(ano, mes, 1),
        'anos': [ano-2, ano-1, ano, ano+1, ano+2],
        'meses': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        # # Gráfico
        'dados': dados,
        # Tabela
        'saldo': round(dados[mes-1], 2),
        'transacoes': transacoes,
    }

    return render(request, 'financeiro/fluxo_de_caixa.html', context)
