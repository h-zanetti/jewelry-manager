import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from pytest_django.asserts import assertContains

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

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

# Editar material
@pytest.fixture
def resposta_editar_material(client, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:editar_material', kwargs={'material_id': material.id}),
        data={
            'material-nome': 'Diamante',
            'material-categoria': 'Pedra',
            'material-qualidade': 10,
            'material-unidades': 3
        }
    )
    return resp

def test_editar_material_status_code(resposta_editar_material):
    assert resposta_editar_material.status_code == 302

def test_material_alterado(resposta_editar_material):
    assert Material.objects.first().qualidade == 10

# Deletar Entrada
@pytest.fixture
def resposta_deletar_material(client, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:deletar_material', kwargs={'material_id': material.id}))
    return resp

def test_deletar_material_status_code(resposta_deletar_material):
    assert resposta_deletar_material.status_code == 302

def test_material_deletada(resposta_deletar_material):
    assert not Material.objects.exists()

def test_entrada_deletada(resposta_deletar_material):
    assert Entrada.objects.exists()

