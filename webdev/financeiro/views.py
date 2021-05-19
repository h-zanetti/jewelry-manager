from dateutil.relativedelta import relativedelta
import datetime as dt
import calendar
from itertools import chain
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from .models import Despesa, Cliente, Venda
from .forms import DespesaForm, ClienteForm, VendaForm

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
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financeiro:despesas')
    else:
        form = DespesaForm()

    context = {
        'title': 'Nova despesa',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def editar_despesa(request, despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id)
    except:
        raise Http404("Despesa não encontrada")

    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('financeiro:despesas')
    else:
        form = DespesaForm(instance=despesa)

    context = {
        'title': 'Editar despesa',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def deletar_despesa(request, despesa_id):
    if request.method == 'POST':
        Despesa.objects.get(id=despesa_id).delete()
    return HttpResponseRedirect(reverse('financeiro:despesas'))

# Clientes
@login_required
def clientes(request):
    context = {
        'title': 'Meus clientes',
        'clientes': Cliente.objects.all()
    }
    return render(request, 'financeiro/clientes.html', context)

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financeiro:clientes')
    else:
        form = ClienteForm()

    context = {
        'title': 'Novo cliente',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def editar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except:
        raise Http404('Cliente não encontrado')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('financeiro:clientes')
    else:
        form = ClienteForm(instance=cliente)

    context = {
        'title': 'Editar cliente',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def deletar_cliente(request, cliente_id):
    if request.method == 'POST':
        Cliente.objects.get(id=cliente_id).delete()
    return HttpResponseRedirect(reverse('financeiro:despesas'))

# Vendas
@login_required
def vendas(request):
    context = {
        'title': 'Vendas Cadastradas',
        'vendas': Venda.objects.all()
    }
    return render(request, 'financeiro/vendas.html', context)

@login_required
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST, initial={'data': timezone.now})
        if form.is_valid():
            venda = form.save()
            ultima_parcela = venda.data + relativedelta(months=venda.parcelas-1)
            venda.ultima_parcela = ultima_parcela
            venda.save()
            return redirect('financeiro:vendas')
    else:
        form = VendaForm(initial={'data': timezone.now})

    context = {
        'title': 'Nova Venda',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def editar_venda(request, venda_id):
    try:
        venda = Venda.objects.get(id=venda_id)
    except:
        raise Http404('Cliente não encontrado')

    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('financeiro:vendas')
    else:
        form = VendaForm(instance=venda)

    context = {
        'title': 'Editar venda',
        'form': form
    }

    return render(request, 'base_form_md.html', context)

@login_required
def deletar_venda(request, venda_id):
    if request.method == 'POST':
        Venda.objects.get(id=venda_id).delete()
    return HttpResponseRedirect(reverse('financeiro:vendas'))

# Fluxo de Caixa
@login_required
def fluxo_de_caixa(request, ano, mes):
    # Fluxo de caixa mensal - Dados da tabela
    vendas_do_mes = Venda.objects.filter(data__year=ano, data__month=mes)
    vendas_anteriores = Venda.objects.filter(
        data__lt=dt.date(ano, mes, 1),
        ultima_parcela__gte=dt.date(ano, mes, 1)
    )
    despesas_do_mes = Despesa.objects.filter(data__year=ano, data__month=mes)
    despesas_fixas = Despesa.objects.filter(repetir__in=['d', 'm'], data__lt=dt.date(ano, mes, 1))
    despesas_anuais = Despesa.objects.filter(repetir='a', data__lt=dt.date(ano, 1, 1), data__month=mes)
    
    # Saldo do mes
    receita = 0
    for venda in chain(vendas_do_mes, vendas_anteriores):
        receita += venda.get_preco_parcela()
    despesas =  0
    for despesa in chain(despesas_do_mes, despesas_fixas, despesas_anuais):
        despesas += despesa.total_pago
    
    # Dados anuais para o gráfico
    # Vendas
    transacoes = sorted(
        chain(vendas_do_mes, vendas_anteriores, despesas_do_mes, despesas_fixas, despesas_anuais),
        key=lambda instance: instance.data
    )
    dados = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    vendas_ano = Venda.objects.filter(data__year=ano)
    for venda in vendas_ano:
        parcelas = venda.get_todas_parcelas()
        for parcela_data in parcelas:
            if parcela_data.year == ano:
                dados[parcela_data.month] += float(parcelas[parcela_data])
    # Despesas variáveis
    despesas_variaveis_ano = Despesa.objects.filter(data__year=ano, repetir='n')
    for despesa in despesas_variaveis_ano:
        dados[despesa.data.month] -= float(despesa.total_pago)
    # Despesas fixas
    despesas_fixas_ano = Despesa.objects.exclude(repetir='n')
    for despesa in despesas_fixas_ano:
        if despesa.repetir == 'a':
            dados[despesa.data.month] -= float(despesa.total_pago)
        elif despesa.repetir == 'm':
            for m in range(despesa.data.month, 13):
                dados[m] -= float(despesa.total_pago)
    
    context = {
        'data': dt.date(ano, mes, 1),
        'saldo': receita - despesas,
        'transacoes': transacoes,
        'nomes': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        'dados': list(dados.values()),
        'anos': [ano-2, ano-1, ano, ano+1, ano+2],
    }

    return render(request, 'financeiro/fluxo_de_caixa.html', context)