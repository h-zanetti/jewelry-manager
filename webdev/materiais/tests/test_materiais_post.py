import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material

# Nova Entrada
@pytest.fixture
def resposta_nova_entrada(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:nova_entrada'),
        data={
            'entrada': '26/04/2021',
            'unidades_compradas': 3,
            'nome': 'Diamante',
            'categoria': 'Pedra',
            'qualidade': 9,
            'total_pago': 1000,
            'estoque': 3
        }
    )
    return resp

def test_nova_entrada_status_code(resposta_nova_entrada):
    assert resposta_nova_entrada.status_code == 302

def test_material_em_estoque(resposta_nova_entrada):
    assert Material.objects.exists()


# Editar material
@pytest.fixture
def material(db):
    return Material.objects.create(
        unidades_compradas=3,
        total_pago=1000,
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        estoque=3,
    )

@pytest.fixture
def resposta_editar_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:editar_material', kwargs={'material_id': material.id}),
        data={
            'entrada': '26/04/2021',
            'unidades_compradas': 3,
            'nome': 'Diamante',
            'categoria': 'Pedra',
            'qualidade': 9,
            'total_pago': 1000,
            'estoque': 3
        }
    )
    return resp

def test_editar_material_status_code(resposta_editar_material):
    assert resposta_editar_material.status_code == 302

def test_material_alterado(resposta_editar_material):
    assert Material.objects.first().nome == "Diamante"

# Deletar Entrada
@pytest.fixture
def resposta_deletar_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:deletar_material', kwargs={'material_id': material.id}))
    return resp

def test_deletar_material_status_code(resposta_deletar_material):
    assert resposta_deletar_material.status_code == 302

def test_material_deletada(resposta_deletar_material):
    assert not Material.objects.exists()
