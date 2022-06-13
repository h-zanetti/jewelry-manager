import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains
from webdev.vendas.models import Cliente
from django.contrib.auth.models import User

@pytest.fixture
def clientes(db):
    return [
        Cliente.objects.create(nome='Pedro', sobrenome="Abster"),
        Cliente.objects.create(nome='Henrique', sobrenome="Damn")
    ]

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_name_response(client, user, clientes):
    client.force_login(user)
    resp = client.get(reverse('vendas:clientes'),
                      data={'search': 'pedro'})
    return resp

def test_filtered_clients_status_code(search_name_response):
    assert search_name_response.status_code == 200

def test_search_client_works(search_name_response, clientes):
    assert clientes[0] in search_name_response.context['clientes']
    assert clientes[1] not in search_name_response.context['clientes']
    