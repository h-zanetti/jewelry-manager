from django.db.models.aggregates import Sum
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

# @pytest.fixture
# def venda(cliente, lista_de_produtos):
#     venda = Venda.objects.create(
#         data=timezone.localdate(),
#         cliente=cliente,
#         parcelas=6,
#         valor=1200
#     )
#     for produto in lista_de_produtos:
#         venda.produtos.add(produto)
#     return venda

# @pytest.fixture
# def lista_de_materiais(db):
#     return [
#         Material.objects.create(nome='Esmeralda', entrada=timezone.localdate(), categoria='Pedra', qualidade=5, estoque=3, unidades_compradas=3, valor=1000,),
#         Material.objects.create(nome='Diamante', entrada=timezone.localdate(), categoria='Pedra', qualidade=8, estoque=3, unidades_compradas=3, valor=75000,),
#         Material.objects.create(nome='Ouro', entrada=timezone.localdate(), categoria='Metal', qualidade=7, estoque=1, unidades_compradas=3, valor=1000,),
#     ]

@pytest.fixture
def receita(db):
    return Receita.objects.create(categoria='Venda')

@pytest.fixture
def lista_de_parcelas(receita):
    parcelas = []
    for m in range(5):
        parcela = Parcela.objects.create(
            data=timezone.localdate(),
            valor= 55 * (1+m),
            receita=receita
        )
        parcelas.append(parcela)
    return parcelas

# Gerar despesas
@pytest.fixture
def lista_de_despesas(db):
    return [
        Despesa.objects.create(data=timezone.localdate(), categoria='Motoboy', valor=150, repetir='n'),
        Despesa.objects.create(data=timezone.localdate(), categoria='MEI', valor=65, repetir='m'),
        Despesa.objects.create(data=timezone.localdate(), categoria='Domínio', valor=65, repetir='a')
    ]

# Visualizar Fluxo de Caixa
@pytest.fixture
def resposta_fluxo_de_caixa(client, lista_de_despesas, lista_de_parcelas):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={'ano': timezone.localdate().year, 'mes': timezone.localdate().month})
    )
    return resp

def test_fluxo_de_caixa_status_code(resposta_fluxo_de_caixa):
    assert resposta_fluxo_de_caixa.status_code == 200

def test_despesas_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_fluxo_de_caixa, despesa.categoria)

def test_parcelas_presente(resposta_fluxo_de_caixa, lista_de_parcelas):
    for parcela in lista_de_parcelas:
        assertContains(resposta_fluxo_de_caixa, parcela.valor)

# def test_vendas_presente(resposta_fluxo_de_caixa, lista_de_vendas):
#     for venda in lista_de_vendas:
#         assertContains(resposta_fluxo_de_caixa, venda.cliente.get_nome_completo())

# def test_entradas_presente(resposta_fluxo_de_caixa, lista_de_materiais):
#     for material in lista_de_materiais:
#         assertContains(resposta_fluxo_de_caixa, material.nome)

def test_saldo_presente(resposta_fluxo_de_caixa):
    receitas = Parcela.objects.filter(
        data__year=timezone.localdate().year,
        data__month=timezone.localdate().month).aggregate(Sum('valor'))['valor__sum']
    despesas = Despesa.objects.filter(
        data__year=timezone.localdate().year,
        data__month=timezone.localdate().month).aggregate(Sum('valor'))['valor__sum']
    saldo = receitas - despesas
    # Formatação -> 1,010.00
    saldo_split = f"{saldo:,.2f}".split('.')
    saldo_str = '.'.join(saldo_split[0].split(','))
    assertContains(resposta_fluxo_de_caixa, f"{saldo_str},{saldo_split[1]}")

# def test_btn_nova_despesa_presente(resposta_fluxo_de_caixa):
#     assertContains(
#         resposta_fluxo_de_caixa,
#         f'href="{reverse("financeiro:nova_despesa")}'
#     )

# def test_btn_nova_venda_presente(resposta_fluxo_de_caixa):
#     assertContains(
#         resposta_fluxo_de_caixa,
#         f'href="{reverse("financeiro:nova_venda")}'
#     )

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
