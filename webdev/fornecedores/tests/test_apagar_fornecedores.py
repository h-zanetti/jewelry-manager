import pytest
from pytest_django.asserts import assertRedirects, assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local, DadosBancarios

# Fornecedores
@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def resposta_autenticada(client, fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_fornecedor', kwargs={'fornecedor_id': fornecedor.id}))
    return resp

def test_apagar_fornecedor_status_code(resposta_autenticada):
    assert resposta_autenticada.status_code == 302

def test_apagar_fornecedor(resposta_autenticada):
    assert not Fornecedor.objects.exists()

def test_apagar_fornecedor_nao_autenticado(client, fornecedor):
    resp = client.post(reverse('fornecedores:deletar_fornecedor', kwargs={'fornecedor_id': fornecedor.id}))
    assert Fornecedor.objects.exists()


# Fornecimentos
@pytest.fixture
def fornecimento(db):
    return Fornecimento.objects.create(nome='fornecimento', qualidade=5)

@pytest.fixture
def resposta_com_fornecimento(client, fornecimento):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_fornecimento', kwargs={'fornecimento_id': fornecimento.id}))
    return resp

def test_apagar_fornecimento_status_code(resposta_com_fornecimento):
    assert resposta_com_fornecimento.status_code == 302

def test_apagar_fornecimento(resposta_com_fornecimento):
    assert not Fornecimento.objects.exists()


# Emails
@pytest.fixture
def email(fornecedor):
    return Email.objects.create(
        fornecedor=fornecedor,
        email='test@email.com'
    )

@pytest.fixture
def resposta_com_email(client, email):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_email', kwargs={'email_id': email.id}))
    return resp

def test_apagar_email_status_code(resposta_com_email):
    assert resposta_com_email.status_code == 302

def test_apagar_email(resposta_com_email):
    assert not Email.objects.exists()


# Telefones
@pytest.fixture
def telefone(fornecedor):
    return Telefone.objects.create(
        fornecedor=fornecedor,
        telefone='11999999999'
    )

@pytest.fixture
def resposta_com_telefone(client, telefone):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_telefone', kwargs={'telefone_id': telefone.id}))
    return resp

def test_apagar_telefone_status_code(resposta_com_telefone):
    assert resposta_com_telefone.status_code == 302

def test_apagar_telefone(resposta_com_telefone):
    assert not Telefone.objects.exists()


# Localizações
@pytest.fixture
def local(fornecedor):
    return Local.objects.create(
        fornecedor=fornecedor,
        pais='Brasil', estado='SP', cidade='São Paulo', bairro='Campo Belo',
        endereco='Rua República do Iraque', cep='04613-031'
    )

@pytest.fixture
def resposta_com_local(client, local):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_local', kwargs={'local_id': local.id}))
    return resp

def test_apagar_telefone_status_code(resposta_com_local):
    assert resposta_com_local.status_code == 302

def test_apagar_telefone(resposta_com_local):
    assert not Local.objects.exists()


# Dados Bancários
@pytest.fixture
def dados_bancarios(fornecedor):
    return DadosBancarios.objects.create(
        fornecedor=fornecedor,
        tipo_de_transacao='px',
        numero='(11) 94464-7420',
    )

@pytest.fixture
def resposta_com_dados_bancarios(client, dados_bancarios):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_dados_bancarios', kwargs={'dados_bancarios_id': dados_bancarios.id}))
    return resp

def test_apagar_dados_bancarios_status_code(resposta_com_dados_bancarios):
    assert resposta_com_dados_bancarios.status_code == 302

def test_apagar_dados_bancarios(resposta_com_dados_bancarios):
    assert not Local.objects.exists()
