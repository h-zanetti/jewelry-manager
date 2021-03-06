import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.vendas.models import Cliente

# Novo Cliente
@pytest.fixture
def resposta_novo_cliente(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('vendas:novo_cliente'),
        data={
            'nome': 'José',
            'sobrenome': 'Azevedo',
            'email': 'Pedro.Azevedo@email.com',
            'telefone': '+5511944440000',
            'endereco': 'R. Lapala',
            'cpf': '00000000000',
            'birth_date': '01-01-2000',
            'observacao': '',
        }
    )
    return resp

def test_novo_cliente_status_code(resposta_novo_cliente):
    assert resposta_novo_cliente.status_code == 302

def test_novo_cliente_criada(resposta_novo_cliente):
    assert Cliente.objects.exists()

# Editar Cliente
@pytest.fixture
def cliente(db):
    return Cliente.objects.create(nome='José', sobrenome='Azevedo')

@pytest.fixture
def resposta_editar_cliente(client, cliente):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('vendas:editar_cliente', kwargs={'cliente_id': cliente.id}),
        data={
            'nome': 'Pedro',
            'sobrenome': 'Azevedo',
        }
    )
    return resp

def test_editar_cliente_status_code(resposta_editar_cliente):
    assert resposta_editar_cliente.status_code == 302

def test_cliente_editada(resposta_editar_cliente):
    assert Cliente.objects.first().nome == 'Pedro'

# Deletar Cliente
@pytest.fixture
def resposta_deletar_cliente(client, cliente):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('vendas:deletar_cliente', kwargs={'cliente_id': cliente.id}))
    return resp

def test_deletar_cliente_status_code(resposta_deletar_cliente):
    assert resposta_deletar_cliente.status_code == 302

def test_cliente_deletada(resposta_deletar_cliente):
    assert not Cliente.objects.exists()

