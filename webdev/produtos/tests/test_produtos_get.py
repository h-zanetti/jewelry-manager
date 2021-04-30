import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects
from webdev.produtos.models import Produto
from django.contrib.auth.models import User

# Estoque
@pytest.fixture
def resposta_estoque_nao_autenticado(client, db):
    resp = client.get(reverse('produtos:estoque'))
    return resp

def test_estoque_produtos_nao_autenticado_status_code(resposta_estoque_nao_autenticado):
    resposta_estoque_nao_autenticado.status_code == 302

@pytest.fixture
def resposta_estoque_autenticado(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque'))
    return resp

def test_estoque_produtos_autenticado_status_code(resposta_estoque_autenticado):
    assert resposta_estoque_autenticado.status_code == 200

@pytest.fixture
def estoque_de_produtos(db):
    return [
        Produto.objects.create(nome='Produto1', colecao="d'Mentira"),
        Produto.objects.create(nome='Produto2', colecao="d'Mentira")
    ]

@pytest.fixture
def resposta_com_estoque(client, estoque_de_produtos):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque'))
    return resp

def test_estoque_de_produtos_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(resposta_com_estoque, produto.nome)

# Novo Produto
@pytest.fixture
def resposta_novo_produto(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:novo_produto'))
    return resp

def test_novo_produto_status_code(resposta_novo_produto):
    assert resposta_novo_produto.status_code == 200

def test_form_present(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<form')

def test_btn_submit_present(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<button type="submit"')

