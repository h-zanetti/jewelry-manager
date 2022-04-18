import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains
from webdev.fornecedores.models import Fornecedor, Fornecimento
from django.contrib.auth.models import User

# Estoque
@pytest.fixture
def fornecedores(db):
    return [
        Fornecedor.objects.create(nome='Zé Comédia'),
        Fornecedor.objects.create(nome='Catateco'),
    ]

@pytest.fixture
def fornecimentos(fornecedores):
    fs = [
        Fornecimento.objects.create(nome='Guarda Ambinhental'),
        Fornecimento.objects.create(nome='Catador')
    ]
    fornecedores[0].fornecimento.add(fs[0])
    fornecedores[1].fornecimento.add(fs[1])
    return fs

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_fornecedor_response(client, user, fornecedores, fornecimentos):
    client.force_login(user)
    resp = client.get(reverse('fornecedores:meus_fornecedores'),
                      data={'search': 'catador'})
    return resp

def test_estoque_produtos_autenticado_status_code(search_fornecedor_response):
    assert search_fornecedor_response.status_code == 200

def test_search_produto_works(search_fornecedor_response):
    assertContains(search_fornecedor_response, 'Catateco')
    assertNotContains(search_fornecedor_response, 'Zé Comédia')
