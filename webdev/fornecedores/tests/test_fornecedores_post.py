import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local, DadosBancarios

# Novo Fornecedor
@pytest.fixture
def fornecimento(db):
    return Fornecimento.objects.create(
        nome="Programador",
        qualidade=10
    )

@pytest.fixture
def resposta_autenticada(client, fornecimento):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_fornecedor'), data={
        'nome': 'Isaac Newton',
        'fornecimento': [fornecimento.id]
    })
    return resp

def test_fornecedor_existe_no_bd(resposta_autenticada):
    assert Fornecedor.objects.exists()

# Novo Fornecimento
@pytest.fixture
def criar_fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def resposta_fornecimento(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_fornecimento', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'nome': 'Fotografia',
        'qualidade': 5
    })
    return resp

def test_fornecimento_existe_no_bd(resposta_fornecimento):
    assert Fornecimento.objects.exists()

def test_fornecimento_nao_autenticado_status_code(client, criar_fornecedor):
    resp = client.post(reverse('fornecedores:novo_fornecimento', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'nome': 'Fotografia',
        'qualidade': 5
    })
    assert resp.status_code == 302


# Novo Email
@pytest.fixture
def resposta_novo_email(client, criar_fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:novo_email', kwargs={'fornecedor_id':criar_fornecedor.id}),
        data={
            'fornecedor': criar_fornecedor.id,
            'email': 'testEmail@gmail.com'
        }
    )
    return resp

def test_email_existe_no_bd(resposta_novo_email):
    assert Email.objects.exists()

# Novo Telefone
@pytest.fixture
def resposta_novo_telefone(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse(
            'fornecedores:novo_telefone',
            kwargs={'fornecedor_id':criar_fornecedor.id}
        ), data={
            'fornecedor': criar_fornecedor.id,
            'telefone': 11944647420
        }
    )
    return resp

def test_telefone_existe_no_bd(resposta_novo_telefone):
    assert Telefone.objects.exists()


# Nova Localização
@pytest.fixture
def resposta_novo_local(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse(
            'fornecedores:novo_local',
            kwargs={'fornecedor_id':criar_fornecedor.id}
        ), data={
            'fornecedor': criar_fornecedor.id,
            'pais': 'Brasil',
            'estado': 'SP',
            'cidade': 'São Paulo',
            'bairro': 'Campo Belo',
            'endereco': 'Av Barão de Vali, 240',
            'cep': '04613-030',
        }
    )
    return resp

def test_local_existe_no_bd(resposta_novo_local):
    assert Local.objects.exists()

# Novos Dados Bancários
@pytest.fixture
def resposta_novos_dados_bancarios(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse(
            'fornecedores:novos_dados_bancarios',
            kwargs={'fornecedor_id':criar_fornecedor.id}
        ), data={
        'fornecedor': criar_fornecedor.id,
        'tipo_de_transacao': 'px',
        'numero': '0000030',
        }
    )
    return resp

def test_dados_bancarios_existe_no_bd(resposta_novos_dados_bancarios):
    assert DadosBancarios.objects.exists()
