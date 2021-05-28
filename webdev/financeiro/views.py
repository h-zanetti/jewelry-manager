# import datetime as dt
# from itertools import chain
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
# from webdev.materiais.models import Material
# from webdev.vendas.models import Venda
from .models import Despesa, Receita
from .forms import CriarDespesaForm, EditarDespesaForm, ReceitaForm

# Receitas
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


# # Fluxo de Caixa
# @login_required
def fluxo_de_caixa(request, ano, mes):
    pass
#     # Fluxo de caixa mensal - Dados da tabela
#     vendas_do_mes = Venda.objects.filter(data__year=ano, data__month=mes)
#     vendas_anteriores = Venda.objects.filter(
#         data__lt=dt.date(ano, mes, 1),
#         ultima_parcela__gte=dt.date(ano, mes, 1)
#     )
#     despesas_do_mes = Despesa.objects.filter(data__year=ano, data__month=mes)
#     despesas_fixas = Despesa.objects.filter(repetir__in=['d', 'm'], data__lt=dt.date(ano, mes, 1))
#     despesas_anuais = Despesa.objects.filter(repetir='a', data__lt=dt.date(ano, 1, 1), data__month=mes)
#     entradas_de_material = Material.objects.filter(entrada__year=ano, entrada__month=mes)

#     # Saldo do mes
#     receita = 0
#     for venda in chain(vendas_do_mes, vendas_anteriores):
#         receita += venda.get_preco_parcela()
#     despesas =  0
#     for despesa in chain(despesas_do_mes, despesas_fixas, despesas_anuais, entradas_de_material):
#         despesas += despesa.total_pago
    
#     # Dados anuais para o gráfico
#     # Vendas
#     def f(instance):
#         tipo_despesa = instance.get_categoria_fluxo_de_caixa().split()[0]
#         if tipo_despesa == 'Entrada':
#             return instance.entrada
#         else: 
#             return instance.data
#     transacoes = sorted(
#         chain(vendas_do_mes, vendas_anteriores, despesas_do_mes, despesas_fixas, despesas_anuais, entradas_de_material),
#         key=lambda instance: f(instance)
#     )
#     dados = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
#     vendas_ano = Venda.objects.filter(data__year=ano)
#     for venda in vendas_ano:
#         parcelas = venda.get_todas_parcelas()
#         for parcela_data in parcelas:
#             if parcela_data.year == ano:
#                 dados[parcela_data.month] += float(parcelas[parcela_data])
    
#     # Entradas de Material
#     materiais_ano = Material.objects.filter(entrada__year=ano)
#     for material in materiais_ano:
#         dados[material.entrada.month] -= float(material.total_pago)

#     # Despesas variáveis
#     despesas_variaveis_ano = Despesa.objects.filter(data__year=ano, repetir='n')
#     for despesa in despesas_variaveis_ano:
#         dados[despesa.data.month] -= float(despesa.total_pago)
    
#     # Despesas fixas
#     despesas_fixas_ano = Despesa.objects.filter(data__year=ano).exclude(repetir='n')
#     for despesa in despesas_fixas_ano:
#         if despesa.repetir == 'a':
#             dados[despesa.data.month] -= float(despesa.total_pago)
#         elif despesa.repetir == 'm':
#             for m in range(despesa.data.month, 13):
#                 dados[m] -= float(despesa.total_pago)
    
#     context = {
#         'data': dt.date(ano, mes, 1),
#         'saldo': receita - despesas,
#         'transacoes': transacoes,
#         'nomes': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
#         'dados': list(dados.values()),
#         'anos': [ano-2, ano-1, ano, ano+1, ano+2],
#     }

#     return render(request, 'financeiro/fluxo_de_caixa.html', context)