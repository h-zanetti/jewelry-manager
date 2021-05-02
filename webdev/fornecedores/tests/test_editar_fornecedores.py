import pytest
from pytest_django.asserts import assertRedirects, assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local

# Editar Fornecedor
@pytest.fixture
def criar_fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def resposta_editar_fornecedor(client, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_fornecedor', kwargs={'fornecedor_id': criar_fornecedor.id}),
        data={'nome': 'Isaac Newton'}
    )
    return resp

def test_status_code(resposta_editar_fornecedor):
    assert resposta_editar_fornecedor.status_code == 302

def test_fornecedor_editado(resposta_editar_fornecedor):
    assert Fornecedor.objects.first().nome == 'Isaac Newton'

def test_editar_fornecedor_nao_autenticado_status_code(client, criar_fornecedor):
    resp = client.post(
        reverse('fornecedores:editar_fornecedor', kwargs={'fornecedor_id': criar_fornecedor.id}),
        data={'nome': 'Isaac Newton'}
    )
    assert resp.status_code == 302


# Editar Fornecimento
@pytest.fixture
def criar_fornecimento(db):
    return Fornecimento.objects.create(nome='Diretor de Arte', qualidade=5)

@pytest.fixture
def resposta_editar_fornecimento(client, criar_fornecimento):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_fornecimento', kwargs={'fornecimento_id': criar_fornecimento.id}),
        data={'nome': 'Fundição', 'qualidade': 2}
    )
    return resp

def test_editar_fornecimento_status_code(resposta_editar_fornecimento):
    assert resposta_editar_fornecimento.status_code == 302

def test_fornecimento_nome_editado(resposta_editar_fornecimento):
    assert Fornecimento.objects.first().nome == 'Fundição'

def test_fornecimento_qualidade_editada(resposta_editar_fornecimento):
    assert Fornecimento.objects.first().qualidade == 2

def test_editar_fornecimento_nao_autenticado_status_code(client, criar_fornecimento):
    resp = client.post(
        reverse('fornecedores:editar_fornecimento', kwargs={'fornecimento_id': criar_fornecimento.id}),
        data={'nome': 'Fundição', 'qualidade': 2}
    )
    assert resp.status_code == 302


# Editar Email
@pytest.fixture
def criar_email(db):
    return Email.objects.create(email='test@email.com')

@pytest.fixture
def resposta_editar_email(client, criar_email):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_email', kwargs={'email_id': criar_email.id}),
        data={'email': 'novo@email.com'}
    )
    return resp

def test_editar_email_status_code(resposta_editar_email):
    assert resposta_editar_email.status_code == 302

def test_email_editado(resposta_editar_email):
    assert Email.objects.first().email == 'novo@email.com'

def test_editar_email_nao_autenticado_status_code(client, criar_email):
    resp = client.post(
        reverse('fornecedores:editar_email', kwargs={'email_id': criar_email.id}),
        data={'email': 'novo@email.com'}
    )
    assert resp.status_code == 302


# Editar Telefone
@pytest.fixture
def criar_telefone(db):
    return Telefone.objects.create(telefone='11944444444')

@pytest.fixture
def resposta_editar_telefone(client, criar_telefone):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_telefone', kwargs={'telefone_id': criar_telefone.id}),
        data={'telefone': '11955555555'}
    )
    return resp

def test_editar_telefone_status_code(resposta_editar_telefone):
    assert resposta_editar_telefone.status_code == 302

def test_telefone_editado(resposta_editar_telefone):
    assert Telefone.objects.first().telefone == '11955555555'

def test_editar_telefone_nao_autenticado_status_code(client, criar_telefone):
    resp = client.post(
        reverse('fornecedores:editar_telefone', kwargs={'telefone_id': criar_telefone.id}),
        data={'telefone': '11955555555'}
    )
    assert resp.status_code == 302


# Editar Localização
@pytest.fixture
def criar_local(db):
    return Local.objects.create(
        pais='Brasil', estado='SP', cidade='São Paulo', bairro='Campo Belo',
        endereco='Rua República do Iraque', cep='04613-031'
    )

@pytest.fixture
def resposta_editar_local(client, criar_local):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_local', kwargs={'local_id': criar_local.id}),
        data={
            'pais': 'Estados Unidos',
            'estado': 'NE',
            'cidade': 'Lincoln',
            'bairro': '',
            'endereco': '1118 Rockhurst Dr.',
            'cep': '68510'
        }
    )
    return resp

def test_editar_local_status_code(resposta_editar_local):
    assert resposta_editar_local.status_code == 302

def test_local_editado(resposta_editar_local):
    assert Local.objects.first().pais == 'Estados Unidos'

def test_editar_local_nao_autenticado_status_code(client, criar_local):
    resp = client.post(
        reverse('fornecedores:editar_local', kwargs={'local_id': criar_local.id}),
        data={
            'pais': 'Estados Unidos',
            'estado': 'NE',
            'cidade': 'Lincoln',
            'bairro': '',
            'endereco': '1118 Rockhurst Dr.',
            'cep': '68510'
        }
    )
    assert resp.status_code == 302

