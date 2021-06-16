from webdev.financeiro.models import Despesa
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from webdev.fornecedores.models import Fornecedor, Servico

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

# Criar
@pytest.fixture
def resposta_novo_servico(client, fornecedor):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:novo_servico'),
        data={
            'nome': 'Fotografia',
            'data': '04-05-2021',
            'fornecedor': fornecedor.id,
            'qualidade': 5,
            'valor': 100.5
        }
    )
    return resp

def test_novo_servico_status_code(resposta_novo_servico):
    assert resposta_novo_servico.status_code == 302

def test_novo_servico_criado(resposta_novo_servico):
    assert Servico.objects.exists()

def test_despesa_criada(resposta_novo_servico):
    assert Despesa.objects.exists()

# Editar
@pytest.fixture
def servico(fornecedor):
    return Servico.objects.create(
        nome='Fotografia',
        data='2021-04-05',
        fornecedor=fornecedor,
        qualidade=5,
        valor=100.5
    )

@pytest.fixture
def resposta_editar_servico(client, servico):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:editar_servico', kwargs={'servico_id': servico.id}),
        data={
            'nome': 'Fotografia',
            'data': '04-05-2021',
            'fornecedor': servico.fornecedor.id,
            'qualidade': 5,
            'valor': 150,
            'despesa': servico.despesa.id
        }
    )
    return resp

def test_editar_servico_status_code(resposta_editar_servico):
    assert resposta_editar_servico.status_code == 302

def test_servico_editado(resposta_editar_servico):
    assert Servico.objects.first().valor == 150

def test_despesa_editada(resposta_editar_servico):
    assert Despesa.objects.first().valor == 150

# Deletar
@pytest.fixture
def resposta_deletar_servico(client, servico):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('fornecedores:deletar_servico', kwargs={'servico_id': servico.id}))
    return resp

def test_deletar_servico_status_code(resposta_deletar_servico):
    assert resposta_deletar_servico.status_code == 302

def test_servico_deletado(resposta_deletar_servico):
    assert not Servico.objects.exists()

