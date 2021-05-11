import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.financeiro.models import Venda, Produto, Cliente

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
def produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

# Nova Venda
@pytest.fixture
def resposta_nova_venda(client, produto, cliente):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('financeiro:nova_venda'),
        data={
            'data': '26-04-2021',
            'cliente': cliente.id,
            'produtos': [produto.id],
            'parcelas': 12,
            'total_pago': 4500
        }
    )
    return resp

def test_nova_venda_status_code(resposta_nova_venda):
    assert resposta_nova_venda.status_code == 302

def test_nova_despesa_criada(resposta_nova_venda):
    assert Venda.objects.exists()

# Editar Venda
@pytest.fixture
def venda(cliente, produto):
    v = Venda.objects.create(
        data='2021-04-26',
        cliente=cliente,
        parcelas=6,
        total_pago=1200
    )
    v.produtos.add(produto)
    return v

@pytest.fixture
def resposta_editar_venda(client, venda, cliente, produto):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('financeiro:editar_venda', kwargs={'venda_id': venda.id}),
        data={
            'data': '26-04-2021',
            'cliente': cliente.id,
            'produtos': [produto.id],
            'parcelas': 6,
            'total_pago': 4500
        }
    )
    return resp

def test_editar_venda_status_code(resposta_editar_venda):
    assert resposta_editar_venda.status_code == 302

def test_venda_editada(resposta_editar_venda):
    assert Venda.objects.first().parcelas == 6

# Deletar Venda
@pytest.fixture
def resposta_deletar_venda(client, venda):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('financeiro:deletar_venda', kwargs={'venda_id': venda.id}))
    return resp

def test_deletar_despesa_status_code(resposta_deletar_venda):
    assert resposta_deletar_venda.status_code == 302

def test_despesa_deletada(resposta_deletar_venda):
    assert not Venda.objects.exists()

