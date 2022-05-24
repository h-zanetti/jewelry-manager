import pytest
from django.urls import reverse
from webdev.produtos.models import Produto
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def produtos(db):
    return [
        Produto.objects.create(nome='Produto1', colecao="d'Mentira"),
        Produto.objects.create(nome='Produto2', colecao="d'Mentira")
    ]

@pytest.fixture
def resposta_sorted_products(client, user, produtos):
    client.force_login(user)
    resp = client.get(reverse('produtos:estoque_produtos'), data={
        'sort-field': 'nome',
        'sort-order': '-',
    })
    return resp

def test_sorted_products_status_code(resposta_sorted_products):
    assert resposta_sorted_products.status_code == 200

def test_products_sorted(resposta_sorted_products):
    assert resposta_sorted_products.context['produtos'][0].nome == 'Produto2'
