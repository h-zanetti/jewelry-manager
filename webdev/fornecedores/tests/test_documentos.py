import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.fornecedores.models import Documento, Fornecedor

@pytest.fixture
def fornecedores(db):
    return [
        Fornecedor.objects.create(nome='Zé Comédia'),
        Fornecedor.objects.create(nome='Catateco'),
    ]

@pytest.fixture
def documentos(fornecedores):
    docs = []
    for f in fornecedores:
        doc = Documento.objects.create(
            fornecedor=f,
            nome='CNPJ',
            numero='00000000'
        )
        docs.append(doc)
    return docs

# Informação disponível
@pytest.fixture
def resposta_com_fornecedores(client, fornecedores, documentos):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:meus_fornecedores'))
    return resp

def test_documento_presente(resposta_com_fornecedores, documentos):
    for doc in documentos:
        assertContains(resposta_com_fornecedores, str(doc))


# Informação editável
@pytest.fixture
def resposta_editar_fornecedor(client, fornecedores):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse(
        'fornecedores:editar_fornecedor',
        kwargs={"fornecedor_id": fornecedores[0].id}
    ))
    return resp

def test_documento_formset_presente(resposta_editar_fornecedor):
    assertContains(resposta_editar_fornecedor, 'Novo documento')