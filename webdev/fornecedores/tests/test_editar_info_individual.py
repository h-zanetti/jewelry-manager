from webdev.fornecedores.tests.test_editar_fornecedor_formset import fornecimento
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local, DadosBancarios

# Editar Email
@pytest.fixture
def criar_fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def criar_email(criar_fornecedor):
    return Email.objects.create(
        fornecedor=criar_fornecedor,
        email='test@email.com'
    )

@pytest.fixture
def resposta_editar_email(client, criar_email, criar_fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_email', kwargs={'email_id': criar_email.id}),
        data={
            'fornecedor': criar_fornecedor.id,
            'email': 'novo@email.com'
        }
    )
    return resp

def test_editar_email_status_code(resposta_editar_email):
    assert resposta_editar_email.status_code == 302

def test_email_editado(resposta_editar_email):
    assert Email.objects.first().email == 'novo@email.com'

# Editar Telefone
@pytest.fixture
def criar_telefone(criar_fornecedor):
    return Telefone.objects.create(
        fornecedor=criar_fornecedor,
        telefone='11944444444'
    )

@pytest.fixture
def resposta_editar_telefone(client, criar_telefone, criar_fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_telefone', kwargs={'telefone_id': criar_telefone.id}),
        data={
            'fornecedor': criar_fornecedor.id,
            'telefone': '11955555555'
        }
    )
    return resp

def test_editar_telefone_status_code(resposta_editar_telefone):
    assert resposta_editar_telefone.status_code == 302

def test_telefone_editado(resposta_editar_telefone):
    assert Telefone.objects.first().telefone == '11955555555'

# Editar Localização
@pytest.fixture
def criar_local(criar_fornecedor):
    return Local.objects.create(
        fornecedor=criar_fornecedor,
        pais='Brasil', estado='SP', cidade='São Paulo', bairro='Campo Belo',
        endereco='Rua República do Iraque', cep='04613-031'
    )

@pytest.fixture
def resposta_editar_local(client, criar_local, criar_fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_local', kwargs={'local_id': criar_local.id}),
        data={
            'fornecedor': criar_fornecedor.id,
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


# Editar Dados Bancários
@pytest.fixture
def criar_dados_bancarios(criar_fornecedor):
    return DadosBancarios.objects.create(
        fornecedor=criar_fornecedor,
        tipo_de_transacao='px',
        numero='(11) 94464-7420',
    )

@pytest.fixture
def resposta_editar_dados_bancarios(client, criar_dados_bancarios, criar_fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_dados_bancarios', kwargs={'dados_bancarios_id': criar_dados_bancarios.id}),
        data={
            'fornecedor': criar_fornecedor.id,
            'tipo_de_transacao': 'dp',
            'banco': 'Nu Bank',
            'agencia': '0001',
            'numero': '444444444444',
        }
    )
    return resp

def test_editar_dados_bancarios_status_code(resposta_editar_dados_bancarios):
    assert resposta_editar_dados_bancarios.status_code == 302

def test_dados_bancarios_editado(resposta_editar_dados_bancarios):
    assert DadosBancarios.objects.first().banco == 'Nu Bank'

