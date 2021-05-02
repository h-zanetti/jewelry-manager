import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local

# Novo Fornecedor
@pytest.fixture
def resposta_autenticada(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_fornecedor'), data={
        'nome': 'Isaac Newton'
    })
    return resp

def test_fornecedor_existe_no_bd(resposta_autenticada):
    assert Fornecedor.objects.exists()

def test_foto_padrao_do_fornecedor(resposta_autenticada):
    assert Fornecedor.objects.first().foto.name == 'default.jpg'

def test_novo_fornecedor_nao_autenticado_status_code(client, db):
    resp = client.post(reverse('fornecedores:novo_fornecedor'), data={
        'nome': 'Isaac Newton'
    })
    assert resp.status_code == 302


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
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_email', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'email': 'testEmail@gmail.com'
    })
    return resp

def test_fornecimento_existe_no_bd(resposta_novo_email):
    assert Email.objects.exists()

def test_fornecimento_nao_autenticado_status_code(client, criar_fornecedor):
    resp = client.post(reverse('fornecedores:novo_email', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'email': 'testEmail@gmail.com'
    })
    assert resp.status_code == 302


# Novo Telefone
@pytest.fixture
def resposta_novo_telefone(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_telefone', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'telefone': 11944647420
    })
    return resp

def test_fornecimento_existe_no_bd(resposta_novo_telefone):
    assert Telefone.objects.exists()

def test_fornecimento_nao_autenticado_status_code(client, criar_fornecedor):
    resp = client.post(reverse('fornecedores:novo_telefone', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'telefone': 11944647420
    })
    assert resp.status_code == 302


# Nova Localização
@pytest.fixture
def resposta_novo_local(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:novo_local', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'pais': 'Brasil',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'bairro': 'Campo Belo',
        'endereco': 'Av Barão de Vali, 240',
        'cep': '04613-030',
    })
    return resp

def test_fornecimento_existe_no_bd(resposta_novo_local):
    assert Local.objects.exists()

def test_fornecimento_nao_autenticado_status_code(client, criar_fornecedor):
    resp = client.post(reverse('fornecedores:novo_local', kwargs={'fornecedor_id':criar_fornecedor.id}), data={
        'pais': 'Brasil',
        'estado': 'SP',
        'cidade': 'São Paulo',
        'bairro': 'Campo Belo',
        'endereco': 'Av Barão de Vali, 240',
        'cep': '04613-030',
    })
    assert resp.status_code == 302
