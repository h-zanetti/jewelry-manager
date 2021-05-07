import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from pytest_django.asserts import assertContains

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

# Nova Entrada
@pytest.fixture
def resposta_nova_entrada(client, fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:nova_entrada'),
        data={
            'entrada-fornecedor': fornecedor.id,
            'entrada-unidades': 3,
            'entrada-total_pago': 1000,
            'material-nome': 'Diamante',
            'material-categoria': 'Pedra',
            'material-qualidade': 9,
            'material-unidades': 3
        }
    )
    return resp

def test_nova_entrada_status_code(resposta_nova_entrada):
    assert resposta_nova_entrada.status_code == 302

def test_entrada_efetuada(resposta_nova_entrada):
    assert Entrada.objects.exists()

def test_material_em_estoque(resposta_nova_entrada):
    assert Material.objects.exists()

# # Editar Entrada
@pytest.fixture
def entrada(db, fornecedor):
    return Entrada.objects.create(fornecedor=fornecedor, unidades=3, total_pago=10000)

@pytest.fixture
def material(db, entrada):
    return Material.objects.create(
        entrada=entrada,
        nome='Diamante',
        categoria='Pedra',
        qualidade=9,
        unidades=3
    )

@pytest.fixture
def resposta_editar_entrada(client, entrada, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:editar_entrada', kwargs={'entrada_id': entrada.id, 'material_id': material.id}),
        data={
            'entrada-fornecedor': entrada.fornecedor.id,
            'entrada-unidades': 5,
            'entrada-total_pago': 1000,
            'material-nome': 'Diamante',
            'material-categoria': 'Pedra',
            'material-qualidade': 10,
            'material-unidades': 3
        }
    )
    return resp

def test_editar_entrada_status_code(resposta_editar_entrada):
    assert resposta_editar_entrada.status_code == 302

def test_entrada_alterada(resposta_editar_entrada):
    assert Entrada.objects.first().unidades == 5

def test_material_alterado(resposta_editar_entrada):
    assert Material.objects.first().qualidade == 10

# Deletar Entrada
@pytest.fixture
def resposta_deletar_entrada(client, entrada, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:deletar_entrada', kwargs={'entrada_id': entrada.id}))
    return resp

def test_deletar_entrada_status_code(resposta_deletar_entrada):
    assert resposta_deletar_entrada.status_code == 302

def test_entrada_deletada(resposta_deletar_entrada):
    assert not Entrada.objects.exists()

def test_material_deletada(resposta_deletar_entrada):
    assert not Material.objects.exists()
