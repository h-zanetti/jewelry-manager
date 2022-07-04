import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains
from django.contrib.auth.models import User
from webdev.vendas.models import Venda, Cliente, Basket, BasketItem, MarkUp
from webdev.produtos.models import Produto

# Visualizar Vendas
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
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def markups(db):
    return [
        MarkUp.objects.create(key='Cliente final', value=3),
        MarkUp.objects.create(key='Atacado', value=1.75),
    ]

@pytest.fixture
def basket(markups):
    return Basket.objects.create(markup=markups[0])

@pytest.fixture
def basket_item(basket, product):
    return BasketItem.objects.create(
        basket=basket,
        product=product,
        quantity=2,
    )

@pytest.fixture
def venda(cliente, basket):
    venda = Venda.objects.create(
        basket=basket,
        data=timezone.now(),
        cliente=cliente,
        parcelas=6,
        valor=1200
    )
    return venda

@pytest.fixture
def resposta_vendas(client, venda):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:minhas_vendas'))
    return resp

def test_vendas_status_code(resposta_vendas):
    assert resposta_vendas.status_code == 200

def test_lista_de_vendas_presente(resposta_vendas, venda):
    assertContains(resposta_vendas, venda.cliente.get_nome_completo())

def test_btn_cadastrar_venda_presente(resposta_vendas):
    assertContains(resposta_vendas, f'<a class="dropdown-item" href="{reverse("vendas:nova_venda")}')

def test_btn_editar_venda_presente(resposta_vendas, venda):
    assertContains(resposta_vendas, f'<a href="{reverse("vendas:editar_venda", kwargs={"venda_id": venda.id})}')

def test_btn_deletar_venda_presente(resposta_vendas, venda):
    assertContains(resposta_vendas, f'<form action="{reverse("vendas:deletar_venda", kwargs={"venda_id": venda.id})}')


# Nova Venda
@pytest.fixture
def resposta_nova_venda(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:novo_cliente'))
    return resp

def test_nova_venda_status_code(resposta_nova_venda):
    assert resposta_nova_venda.status_code == 200

def test_form_presente(resposta_nova_venda):
    assertContains(resposta_nova_venda, f'<form')

def test_btn_submit_stay_presente(resposta_nova_venda):
    assertContains(resposta_nova_venda, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_nova_venda):
    assertContains(resposta_nova_venda, f'<button type="submit" name="submit-leave"')


# Editar Venda
@pytest.fixture
def resposta_editar_venda(client, venda):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:editar_venda', kwargs={'venda_id': venda.id}))
    return resp

def test_editar_venda_status_code(resposta_editar_venda):
    assert resposta_editar_venda.status_code == 200

def test_form_editar_venda_presente(resposta_editar_venda):
    assertContains(resposta_editar_venda, f'<form')

def test_btn_submit_stay_nao_presente(resposta_editar_venda):
    assertNotContains(resposta_editar_venda, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_editar_venda):
    assertContains(resposta_editar_venda, f'<button type="submit" name="submit-leave"')

def test_receita_presente_e_escondida(resposta_editar_venda, venda):
    assertContains(resposta_editar_venda, f'<input type="hidden" name="receita" value="{venda.receita.id}"')
