import os
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains, assertRedirects
from webdev.fornecedores.models import Fornecedor, Documento, Fornecimento, Email, Telefone, Local, DadosBancarios

# Botões presentes (GET)
@pytest.fixture
def resposta_fornecedores(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:meus_fornecedores'))
    return resp

def test_btn_exportar_fornecedores_presente(resposta_fornecedores):
    assertContains(resposta_fornecedores, f'href="{reverse("fornecedores:exportar_fornecedores")}')

def test_btn_importar_fornecedores_presente(resposta_fornecedores):
    assertContains(resposta_fornecedores, f'href="{reverse("fornecedores:importar_fornecedores")}')

# Importação de fornecedores (POST)
@pytest.fixture
def resposta_importar_fornecedores(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    with open(os.path.join(os.path.dirname(__file__), 'importacoes/fornecedores.xls'), 'rb') as xl_file:
        resp = client.post(
            reverse('fornecedores:importar_fornecedores'),
            data={'myfile': xl_file}
        )
        xl_file.close()
    return resp

def test_import_redirection(resposta_importar_fornecedores):
    assertRedirects(resposta_importar_fornecedores, reverse('fornecedores:meus_fornecedores'))

def test_fornecedor_importado(resposta_importar_fornecedores):
    assert Fornecedor.objects.exists()

def test_fornecimento_importado(resposta_importar_fornecedores):
    assert Fornecimento.objects.exists()

def test_documento_importado(resposta_importar_fornecedores):
    assert Documento.objects.exists()

def test_email_importado(resposta_importar_fornecedores):
    assert Email.objects.exists()

def test_local_importado(resposta_importar_fornecedores):
    assert Local.objects.exists()

def test_dados_bancarios_importado(resposta_importar_fornecedores):
    assert DadosBancarios.objects.exists()

def test_telefone_importado(resposta_importar_fornecedores):
    assert Telefone.objects.exists()
