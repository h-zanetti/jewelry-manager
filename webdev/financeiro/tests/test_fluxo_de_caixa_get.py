import pytest
import datetime as dt
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.financeiro.models import Despesa
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

@pytest.fixture
def lista_de_vendas(cliente, lista_de_produtos):
    vendas = []
    for produto in lista_de_produtos:
        venda = Venda.objects.create(
            data=timezone.now(),
            cliente=cliente,
            parcelas=6,
            ultima_parcela=dt.date(timezone.now().year, timezone.now().month + 5, timezone.now().day),
            total_pago=1200
        )
        venda.produtos.add(produto)
        vendas.append(venda)
    return vendas

@pytest.fixture
def lista_de_despesas(db):
    return [
        Despesa.objects.create(data=timezone.now(), categoria='Motoboy', total_pago=150, repetir='n'),
        Despesa.objects.create(data=timezone.now(), categoria='MEI', total_pago=65, repetir='m'),
        Despesa.objects.create(data=timezone.now(), categoria='Domínio', total_pago=65, repetir='a')
    ]

@pytest.fixture
def lista_de_materiais(db):
    return [
        Material.objects.create(nome='Esmeralda', entrada=timezone.now(), categoria='Pedra', qualidade=5, estoque=3, unidades_compradas=3, total_pago=1000,),
        Material.objects.create(nome='Diamante', entrada=timezone.now(), categoria='Pedra', qualidade=8, estoque=3, unidades_compradas=3, total_pago=75000,),
        Material.objects.create(nome='Ouro', entrada=timezone.now(), categoria='Metal', qualidade=7, estoque=1, unidades_compradas=3, total_pago=1000,),
    ]

# Visualizar Fluxo de Caixa
@pytest.fixture
def resposta_fluxo_de_caixa(client, lista_de_vendas, lista_de_despesas, lista_de_materiais):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={'ano': timezone.now().year, 'mes': timezone.now().month})
    )
    return resp

def test_fluxo_de_caixa_status_code(resposta_fluxo_de_caixa):
    assert resposta_fluxo_de_caixa.status_code == 200

def test_despesas_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_fluxo_de_caixa, despesa.categoria)

def test_vendas_presente(resposta_fluxo_de_caixa, lista_de_vendas):
    for venda in lista_de_vendas:
        assertContains(resposta_fluxo_de_caixa, venda.cliente.get_nome_completo())

def test_entradas_presente(resposta_fluxo_de_caixa, lista_de_materiais):
    for material in lista_de_materiais:
        assertContains(resposta_fluxo_de_caixa, material.nome)

def test_saldo_presente(resposta_fluxo_de_caixa, lista_de_vendas, lista_de_despesas, lista_de_materiais):
    receitas = []
    for venda in lista_de_vendas:
        receitas.append(venda.get_preco_parcela())
    despesas = []
    for despesa in lista_de_despesas:
        despesas.append(despesa.total_pago)
    for material in lista_de_materiais:
        despesas.append(material.total_pago)
    saldo = sum(receitas) - sum(despesas)
    saldo_split = f"{saldo:,.2f}".split('.')
    saldo_str = '.'.join(saldo_split[0].split(','))
    assertContains(resposta_fluxo_de_caixa, f"{saldo_str},{saldo_split[1]}")

def test_btn_nova_despesa_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("financeiro:nova_despesa")}'
    )

def test_btn_nova_venda_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("financeiro:nova_venda")}'
    )

def test_btn_visualizar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'href="#ModalVisualizarDespesa{despesa.id}'
        )

def test_btn_visualizar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
    for venda in lista_de_vendas:
        assertContains(
            resposta_fluxo_de_caixa, f'href="#ModalVisualizarDespesa{venda.id}'
        )

def test_btn_editar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'<a href="{reverse("financeiro:editar_despesa", kwargs={"despesa_id": despesa.id})}'
        )

def test_btn_editar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
    for venda in lista_de_vendas:
        assertContains(
            resposta_fluxo_de_caixa, f'<a href="{reverse("financeiro:editar_venda", kwargs={"venda_id": venda.id})}'
        )

def test_btn_deletar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'<form action="{reverse("financeiro:deletar_despesa", kwargs={"despesa_id": despesa.id})}'
        )

def test_btn_deletar_venda_presente(resposta_fluxo_de_caixa, lista_de_vendas):
    for venda in lista_de_vendas:
        assertContains(
            resposta_fluxo_de_caixa, f'<form action="{reverse("financeiro:deletar_venda", kwargs={"venda_id": venda.id})}'
        )
