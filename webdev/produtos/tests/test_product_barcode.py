import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.produtos.models import Produto
from pytest_django.asserts import assertContains, assertNotContains

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def produtos(db):
    return [
        Produto.objects.create(nome='Produto1', colecao='Pedra'),
        Produto.objects.create(nome='Produto2', colecao='Pedra'),
        Produto.objects.create(nome='Produto3', colecao='Metal'),
        Produto.objects.create(nome='Produto4', colecao='Metal'),
    ]

# GET produto barcode page
@pytest.fixture
def produto_barcode_response(client, user, produtos):
    client.force_login(user)
    resp = client.get(reverse('produtos:product_barcode'), data={
        'produtos': '[1, 2]',
    })
    return resp

def test_produto_barcode_status_code(produto_barcode_response):
    assert produto_barcode_response.status_code == 200

def test_produtos_present(produto_barcode_response, produtos):
    for produto in produtos[:2]:
        assertContains(produto_barcode_response, produto.nome)

def test_produtos_filtered_out(produto_barcode_response, produtos):
    for produto in produtos[-2:]:
        assertNotContains(produto_barcode_response, produto.nome)
