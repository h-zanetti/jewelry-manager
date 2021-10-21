from webdev.financeiro.models import Despesa
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from webdev.fornecedores.models import Fornecedor

# Editar material
@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
    )

@pytest.fixture
def resposta_form_editar_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    return client.get(
        reverse('materiais:editar_material',
        kwargs={'material_id': material.id})
    )

def test_get_editar_material_status_code(resposta_form_editar_material):
    assert resposta_form_editar_material.status_code == 200

@pytest.fixture
def resposta_editar_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:editar_material', kwargs={'material_id': material.id}),
        data={
            'foto': material.foto.url,
            'nome': 'Esmeralda',
            'categoria': 'Pedra',
            'qualidade': 9,
        }
    )
    return resp

def test_editar_material_status_code(resposta_editar_material):
    assert resposta_editar_material.status_code == 302

def test_material_alterado(resposta_editar_material):
    assert Material.objects.first().qualidade == 9

# Deletar Entrada
@pytest.fixture
def resposta_deletar_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    return client.post(
        reverse('materiais:deletar_material',
        kwargs={'material_id': material.id})
    )

def test_deletar_material_status_code(resposta_deletar_material):
    assert resposta_deletar_material.status_code == 302

def test_material_deletada(resposta_deletar_material):
    assert not Material.objects.exists()
