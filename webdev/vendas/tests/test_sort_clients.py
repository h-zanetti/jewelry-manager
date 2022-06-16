import pytest
from django.urls import reverse
from webdev.vendas.models import Cliente
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def clientes(db):
    return [
        Cliente.objects.create(nome='Pedro', sobrenome="Abster"),
        Cliente.objects.create(nome='Henrique', sobrenome="Damn")
    ]

@pytest.fixture
def resposta_sorted_clients(client, user, clientes):
    client.force_login(user)
    resp = client.get(reverse('vendas:clientes'), data={
        'sort-field': 'sobrenome',
        'sort-order': '-',
    })
    return resp

def test_sorted_clients_status_code(resposta_sorted_clients):
    assert resposta_sorted_clients.status_code == 200

def test_clients_sorted(resposta_sorted_clients):
    assert resposta_sorted_clients.context['clientes'][0].nome == 'Henrique'
