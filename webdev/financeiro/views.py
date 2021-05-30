import datetime as dt
from itertools import chain
from django.db.models.aggregates import Sum
from django.db.models.functions.datetime import TruncMonth
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
    # Dados do gráfico
    parcelas_do_ano = Parcela.objects.filter(data__year=ano).annotate(month=TruncMonth('data')).values('month').annotate(valor=Sum('valor'))
    despesas_do_ano = Despesa.objects.filter(data__year=ano).annotate(month=TruncMonth('data')).values('month').annotate(valor=Sum('valor'))
    dados = []
    for m in range(1, 13):
        receita_mes = parcelas_do_ano.filter(month__month=m).aggregate(Sum('valor'))['valor__sum']
        receita_mes = 0 if receita_mes == None else float(receita_mes)
        despesa_do_mes = despesas_do_ano.filter(month__month=m).aggregate(Sum('valor'))['valor__sum']
        despesa_do_mes = 0 if despesa_do_mes == None else float(despesa_do_mes)
        dados.append(receita_mes - despesa_do_mes)
    # Fluxo de caixa mensal - Dados da tabela
    receita = Parcela.objects.filter(data__year=ano, data__month=mes)
    despesas = Despesa.objects.filter(data__year=ano, data__month=mes)
    transacoes = sorted(
        chain(receita, despesas),
        key=lambda instance: instance.data
    )
    # Saldo do mes
    receitas_sum = receita.aggregate(Sum('valor'))['valor__sum']
    receitas_sum = 0 if receitas_sum == None else float(receitas_sum)
    despesas_sum = despesas.aggregate(Sum('valor'))['valor__sum']
    despesas_sum = 0 if despesas_sum == None else float(despesas_sum)
    saldo = receitas_sum - despesas_sum

    context = {
        # Data da requisição
        'data': dt.date(ano, mes, 1),
        'anos': [ano-2, ano-1, ano, ano+1, ano+2],
        # Gráfico
        'nomes': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'dados': dados,
        # Tabela
        'saldo': saldo,
        'transacoes': transacoes,
    }

    return render(request, 'financeiro/fluxo_de_caixa.html', context)