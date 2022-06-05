import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains
from webdev.produtos.models import Produto
from django.contrib.auth.models import User

# Estoque
@pytest.fixture
def produtos(db):
    return [
        Produto.objects.create(nome='Produto 1', colecao="d'Mentira"),
        Produto.objects.create(nome='Anel Legal', colecao="d'Mentira"),
    ]

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_name_response(client, user, produtos):
    client.force_login(user)
    resp = client.get(reverse('produtos:estoque_produtos'),
                      data={'search': 'produto'})
    return resp

def test_estoque_produtos_autenticado_status_code(search_name_response):
    assert search_name_response.status_code == 200

def test_search_produto_works(search_name_response):
    assertContains(search_name_response, 'Produto 1')
    assertNotContains(search_name_response, 'Anel Legal')
