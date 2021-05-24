import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Fornecimento, Email, Telefone, Local, DadosBancarios, Documento

@pytest.fixture
def fornecimento(db):
    return Fornecimento.objects.create(
        nome='Acabamento',
        qualidade=7
    )

@pytest.fixture
def criar_fornecedor(fornecimento):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def resposta_editar_fornecedor_get(client, criar_fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:editar_fornecedor', kwargs={'fornecedor_id': criar_fornecedor.id}))
    return resp

def test_editar_fornecedor_status_code(resposta_editar_fornecedor_get):
    assert resposta_editar_fornecedor_get.status_code == 200

def test_email_formset_presente(resposta_editar_fornecedor_get):
    assertContains(
        resposta_editar_fornecedor_get,
        '<input type="hidden" name="email-TOTAL_FORMS"'
    )

def test_telefone_formset_presente(resposta_editar_fornecedor_get):
    assertContains(
        resposta_editar_fornecedor_get,
        '<input type="hidden" name="telefone-TOTAL_FORMS"'
    )

def test_dados_bancarios_formset_presente(resposta_editar_fornecedor_get):
    assertContains(
        resposta_editar_fornecedor_get,
        '<input type="hidden" name="dados_bancarios-TOTAL_FORMS"'
    )

def test_documentos_formset_presente(resposta_editar_fornecedor_get):
    assertContains(
        resposta_editar_fornecedor_get,
        '<input type="hidden" name="documento-TOTAL_FORMS"'
    )

def test_local_formset_presente(resposta_editar_fornecedor_get):
    assertContains(
        resposta_editar_fornecedor_get,
        '<input type="hidden" name="local-TOTAL_FORMS"'
    )

@pytest.fixture
def resposta_editar_fornecedor(client, criar_fornecedor, fornecimento):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_fornecedor', kwargs={'fornecedor_id': criar_fornecedor.id}),
        data={
            # Dados do fornecedor
            'fornecedor-nome': 'Isaac Newton',
            'fornecedor-fornecimento': [fornecimento.id],
            # Emails
            "email-TOTAL_FORMS": "1",
            "email-INITIAL_FORMS": "0",
            "email-MIN_NUM_FORMS": "0",
            "email-MAX_NUM_FORMS": "1000",
            'email-0-email': 'IsaacNewton@gmail.com',
            # Telefones
            "telefone-TOTAL_FORMS": "1",
            "telefone-INITIAL_FORMS": "0",
            "telefone-MIN_NUM_FORMS": "0",
            "telefone-MAX_NUM_FORMS": "1000",
            'telefone-0-telefone': '91100000000',
            # Dados bancarios
            "dados_bancarios-TOTAL_FORMS": "1",
            "dados_bancarios-INITIAL_FORMS": "0",
            "dados_bancarios-MIN_NUM_FORMS": "0",
            "dados_bancarios-MAX_NUM_FORMS": "1000",
            'dados_bancarios-0-tipo_de_transacao': 'dp',
            'dados_bancarios-0-banco': 'Nu Bank',
            'dados_bancarios-0-agencia': '0001',
            'dados_bancarios-0-numero': '123456',
            # Documentos
            "documento-TOTAL_FORMS": "1",
            "documento-INITIAL_FORMS": "0",
            "documento-MIN_NUM_FORMS": "0",
            "documento-MAX_NUM_FORMS": "1000",
            'documento-0-nome': 'CNPJ',
            'documento-0-numero': '1234567890-12',
            # Localizacoes
            "local-TOTAL_FORMS": "1",
            "local-INITIAL_FORMS": "0",
            "local-MIN_NUM_FORMS": "0",
            "local-MAX_NUM_FORMS": "1000",
            'local-0-cidade': 'São Paulo',
            'local-0-estado': 'SP',
            'local-0-pais': 'Brasil',
            'local-0-cep': '04613-030',
            'local-0-bairro': 'Campo Belo',
            'local-0-endereco': 'Av. Republica do Iraque, 123',
        }
    )
    return resp

def test_status_code(resposta_editar_fornecedor):
    assert resposta_editar_fornecedor.status_code == 302

def test_fornecimento_editado(resposta_editar_fornecedor):
    novo_fornecedor = Fornecedor.objects.first()
    assert len(novo_fornecedor.fornecimento.all()) > 0

def test_fornecedor_editado(resposta_editar_fornecedor):
    assert Fornecedor.objects.first().nome == 'Isaac Newton'

def test_email_adicionado(resposta_editar_fornecedor):
    assert Email.objects.exists()

def test_telefone_adicionado(resposta_editar_fornecedor):
    assert Telefone.objects.exists()

def test_dados_bancarios_adicionado(resposta_editar_fornecedor):
    assert DadosBancarios.objects.exists()

def test_documento_adicionado(resposta_editar_fornecedor):
    assert Documento.objects.exists()

def test_local_adicionado(resposta_editar_fornecedor):
    assert Local.objects.exists()
