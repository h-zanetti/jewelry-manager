from calendar import monthrange
import datetime as dt
from itertools import chain
from django.db.models.aggregates import Sum
from django.db.models.functions.datetime import TruncMonth
from django.db.models.query_utils import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from .models import Despesa, Parcela, Receita
from .forms import CriarDespesaForm, EditarDespesaForm, ReceitaForm

# Receitas
@login_required
def receitas(request):
    context = {
        'title': 'Minhas receitas',
        'receitas': Receita.objects.all()
    }
    return render(request, 'financeiro/receitas.html', context)

@login_required
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

@login_required
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

@login_required
def deletar_receita(request, receita_id):
    if request.method == 'POST':
        Receita.objects.get(id=receita_id).delete()
    return HttpResponseRedirect(reverse('financeiro:receitas'))

# Despesas
@login_required
def despesas(request):
    context = {
        'title': 'Minhas despesas',
        'despesas': Despesa.objects.all()
    }
    return render(request, 'financeiro/despesas.html', context)

@login_required
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

@login_required
def editar_despesa(request, despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id)
    except:
        raise Http404("Despesa não encontrada")

    if request.method == 'POST':
        form = EditarDespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            despesa_edt = form.save()
            if not despesa_edt.is_active and despesa_edt.data_de_encerramento == None and despesa_edt.repetir:
                despesa_edt.data_de_encerramento = timezone.localdate()
                despesa_edt.save()
            return redirect('financeiro:despesas')
    else:
        form = EditarDespesaForm(instance=despesa)

    context = {
        'title': 'Editar despesa',
        'form': form,
    }

    return render(request, 'financeiro/form_despesa.html', context)

@login_required
def deletar_despesa(request, despesa_id):
    if request.method == 'POST':
        Despesa.objects.get(id=despesa_id).delete()
    return HttpResponseRedirect(reverse('financeiro:despesas'))


# Fluxo de Caixa
@login_required
def fluxo_de_caixa(request, ano, mes):
    # Dados do gráfico - Fluxo de caixa anual
    parcelas_do_ano = Parcela.objects.filter(data__year=ano).annotate(month=TruncMonth('data')).values('month').annotate(valor=Sum('valor'))
    despesas_variaveis_do_ano = Despesa.objects.filter(repetir='', data__year=ano)
    despesas_fixas_do_ano = Despesa.objects.exclude(repetir='').filter(
        Q(is_active=True) | Q(data_de_encerramento__year__gte=ano),
        data__year__lte=ano
    )
    dados = []
    for m in range(1, 13):
        # Receita
        receita_mes = parcelas_do_ano.filter(month__month=m).aggregate(Sum('valor'))['valor__sum']
        receita_mes = 0 if receita_mes == None else float(receita_mes)
        # Despesas Variáveis
        despesas_variaveis_mes = despesas_variaveis_do_ano.filter(data__month=m).aggregate(Sum('valor'))['valor__sum']
        despesas_variaveis_mes = 0 if despesas_variaveis_mes == None else float(despesas_variaveis_mes)
        # Despesas Fixas
        despesas_fixas_mensais = despesas_fixas_do_ano.filter(
            Q(is_active=True) | Q(data_de_encerramento__gte=dt.date(ano, m, 1)),
            data__month__lte=m,
            repetir='m',
        ).aggregate(Sum('valor'))['valor__sum']
        despesas_fixas_mensais = 0 if despesas_fixas_mensais == None else float(despesas_fixas_mensais)
        despesas_fixas_anuais = despesas_fixas_do_ano.filter(
            Q(is_active=True) | Q(data_de_encerramento__gte=dt.date(ano, m, 1)),
            data__month=m,
            repetir='a',
        ).aggregate(Sum('valor'))['valor__sum']
        despesas_fixas_anuais = 0 if despesas_fixas_anuais == None else float(despesas_fixas_anuais)
        despesas_mes = despesas_variaveis_mes + despesas_fixas_mensais + despesas_fixas_anuais
        dados.append(receita_mes - despesas_mes)
    # Dados da tabela - Fluxo de caixa mensal
    parcelas = Parcela.objects.filter(data__year=ano, data__month=mes)
    despesas_variaveis = Despesa.objects.filter(repetir='', data__year=ano, data__month=mes)
    despesas_mensais = Despesa.objects.filter(repetir='m', is_active=True, data__lte=f'{ano}-{mes}-{monthrange(ano, mes)[1]}')
    despesas_anuais = Despesa.objects.filter(repetir='a', is_active=True, data__lte=f'{ano}-{mes}-{monthrange(ano, mes)[1]}')
    transacoes = sorted(
        chain(parcelas, despesas_variaveis, despesas_mensais, despesas_anuais),
        key=lambda instance: instance.data
    )
    # Calculo de Saldo
    # Receitas
    receitas_sum = parcelas.aggregate(Sum('valor'))['valor__sum']
    receitas_sum = 0 if receitas_sum == None else float(receitas_sum)
    # Despesas variaveis
    despesas_variaveis_sum = despesas_variaveis.aggregate(Sum('valor'))['valor__sum']
    despesas_variaveis_sum = 0 if despesas_variaveis_sum == None else float(despesas_variaveis_sum)
    # Despesas mensais
    despesas_mensais_sum = despesas_mensais.aggregate(Sum('valor'))['valor__sum']
    despesas_mensais_sum = 0 if despesas_mensais_sum == None else float(despesas_mensais_sum)
    # Despesas anuais
    despesas_anuais_sum = despesas_anuais.aggregate(Sum('valor'))['valor__sum']
    despesas_anuais_sum = 0 if despesas_anuais_sum == None else float(despesas_anuais_sum)
    despesas_sum = despesas_mensais_sum + despesas_anuais_sum + despesas_variaveis_sum
    saldo = receitas_sum - despesas_sum

    context = {
        # Data da requisição
        'data': dt.date(ano, mes, 1),
        'anos': [ano-2, ano-1, ano, ano+1, ano+2],
        'meses': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        # # Gráfico
        'dados': dados,
        # Tabela
        'saldo': saldo,
        'transacoes': transacoes,
    }

    return render(request, 'financeiro/fluxo_de_caixa.html', context)