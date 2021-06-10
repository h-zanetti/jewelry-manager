from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.db.models.aggregates import Sum
from django.db.models.query_utils import refs_expression
import pytest
import datetime as dt
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.financeiro.models import Despesa, Parcela, Receita
from webdev.vendas.models import Cliente, Venda
from webdev.produtos.models import Produto
from webdev.materiais.models import Material

@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        nome="Henrique",
        sobrenome="Navaz",
        email="henrique.navaz@gmail.com",
        telefone="11966647420",
        endereco="Av. Localiza Aí Bebê, 240, Campo Belo, São Paulo, SP, 04613-030"
    )

@pytest.fixture
def lista_de_produtos(db):
    return [
        Produto.objects.create(nome='Anel', colecao="d'Mentira"),
        Produto.objects.create(nome='Brinco', colecao="d'Mentira"),
        Produto.objects.create(nome='Bracelete', colecao="d'Mentira")
    ]

'''
Objetos do tipo Parcela e Receita são criados, edidatos ou deletados automaticamente ao salvar, editar ou 
deletar um objeto do tipo Venda. Para mais informações, ver tests do arquivo test_vendas_post.py ou as 
funções em webdev.financeiro.signals
'''
@pytest.fixture
def venda(cliente, lista_de_produtos):
    venda = Venda.objects.create(
        data=timezone.localdate(),
        cliente=cliente,
        parcelas=6,
        valor=1200
    )
    for produto in lista_de_produtos:
        venda.produtos.add(produto)
    return venda

# Gerar despesas
@pytest.fixture
def lista_de_despesas(db):
    return [
        Despesa.objects.create(data=timezone.localdate(), categoria='Motoboy', valor=150, repetir=''),
        Despesa.objects.create(data=timezone.localdate(), categoria='MEI', valor=50, repetir='m'),
        Despesa.objects.create(
            data=timezone.localdate() - relativedelta(years=1), # Despesa criada para testar repetições anuais
            categoria='Domínio', valor=95, repetir='a'),
        Despesa.objects.create(
            data=timezone.localdate() - relativedelta(months=1), # Despesa criada para testar repetições mensais
            categoria='Conta de Luz', valor=200, repetir='m'),
    ]
    
# @pytest.fixture
# def lista_de_materiais(db):
#     return [
#         Material.objects.create(nome='Esmeralda', entrada=timezone.localdate(), categoria='Pedra', qualidade=5, estoque=3, unidades_compradas=3, valor=1000,),
#         Material.objects.create(nome='Diamante', entrada=timezone.localdate(), categoria='Pedra', qualidade=8, estoque=3, unidades_compradas=3, valor=75000,),
#         Material.objects.create(nome='Ouro', entrada=timezone.localdate(), categoria='Metal', qualidade=7, estoque=1, unidades_compradas=3, valor=1000,),
#     ]

# Visualizar Fluxo de Caixa
@pytest.fixture
def resposta_fluxo_de_caixa(client, lista_de_despesas, venda):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={'ano': timezone.localdate().year, 'mes': timezone.localdate().month})
    )
    return resp

def test_fluxo_de_caixa_status_code(resposta_fluxo_de_caixa):
    assert resposta_fluxo_de_caixa.status_code == 200

# Tabela
def test_despesas_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_fluxo_de_caixa, despesa.categoria)

def test_parcelas_presente(resposta_fluxo_de_caixa, venda):
    # Formatar parcela -> 1,010.10
    valor = ','.join(str(round(venda.get_valor_parcela(), 2)).split('.'))
    assertContains(resposta_fluxo_de_caixa, valor)

def test_vendas_presente(resposta_fluxo_de_caixa, venda):
    assertContains(resposta_fluxo_de_caixa, venda.cliente.get_nome_completo())

# def test_materiais_presente(resposta_fluxo_de_caixa, lista_de_materiais):
#     for material in lista_de_materiais:
#         assertContains(resposta_fluxo_de_caixa, material.nome)

def test_saldo_presente(resposta_fluxo_de_caixa):
    current_dt = timezone.localdate()
    # Receitas
    receitas = Parcela.objects.filter(
        data__year=current_dt.year,
        data__month=current_dt.month).aggregate(Sum('valor'))['valor__sum']
    # Despesas Variaveis
    despesas_variaveis = Despesa.objects.filter(
        repetir='',
        data__year=current_dt.year,
        data__month=current_dt.month).aggregate(Sum('valor'))['valor__sum']
    despesas_variaveis_sum = 0 if despesas_variaveis == None else float(despesas_variaveis)
    # Despesas Fixas
    despesas_mensais = Despesa.objects.filter(
        repetir='m',
        data__lte=current_dt,
        ).aggregate(Sum('valor'))['valor__sum']
    despesas_mensais_sum = 0 if despesas_mensais == None else float(despesas_mensais)
    despesas_anuais = Despesa.objects.filter(
        repetir='a',
        data__month=current_dt.month,
        data__year__lte=current_dt.year).aggregate(Sum('valor'))['valor__sum']
    despesas_anuais_sum = 0 if despesas_anuais == None else float(despesas_anuais)
    # Saldo
    despesas = despesas_variaveis_sum + despesas_mensais_sum + despesas_anuais_sum
    saldo = float(receitas) - despesas
    # Formatação -> 1,010.00
    saldo_split = f"{saldo:,.2f}".split('.')
    saldo_str = ','.join(saldo_split)
    assertContains(resposta_fluxo_de_caixa, saldo_str)

# Gráfico
def test_dados_do_grafico_corretos(resposta_fluxo_de_caixa, lista_de_despesas):
    # dados = [0, 0, 0, 0, -200, -295, -50, -50, -50, -50, -50, -250]
    dados = [0,0,0,0,0,0,0,0,0,0,0,0]
    for parcela in Parcela.objects.all():
        dados[parcela.data.month-1] += float(parcela.valor)
    for despesa in lista_de_despesas:
        if despesa.repetir == 'm':
            for mes in range(despesa.data.month, 13):
                i = mes - 1
                dados[i] -= float(despesa.valor)
        else:
            i = despesa.data.month - 1
            dados[i] -= float(despesa.valor)
    assert resposta_fluxo_de_caixa.context['dados'] == dados

# Botões
def test_btn_nova_despesa_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("financeiro:nova_despesa")}'
    )

def test_btn_nova_venda_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("vendas:nova_venda")}'
    )

# def test_btn_visualizar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
#     for despesa in lista_de_despesas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'href="#ModalVisualizarDespesa{despesa.id}'
#         )

# def test_btn_visualizar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
#     for venda in lista_de_vendas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'href="#ModalVisualizarDespesa{venda.id}'
#         )

# def test_btn_editar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
#     for despesa in lista_de_despesas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'<a href="{reverse("financeiro:editar_despesa", kwargs={"despesa_id": despesa.id})}'
#         )

# def test_btn_editar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
#     for venda in lista_de_vendas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'<a href="{reverse("financeiro:editar_venda", kwargs={"venda_id": venda.id})}'
#         )

# def test_btn_deletar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
#     for despesa in lista_de_despesas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'<form action="{reverse("financeiro:deletar_despesa", kwargs={"despesa_id": despesa.id})}'
#         )

# def test_btn_deletar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
#     for venda in lista_de_vendas:
#         assertContains(
#             resposta_fluxo_de_caixa, f'<form action="{reverse("financeiro:deletar_venda", kwargs={"venda_id": venda.id})}'
#         )
