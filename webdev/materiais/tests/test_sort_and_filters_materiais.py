import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains
from webdev.materiais.models import Material
from django.contrib.auth.models import User

@pytest.fixture
def materiais(db):
    return [
        Material.objects.create(nome='Diamante', categoria='Pedra'),
        Material.objects.create(nome='Esmeralda', categoria='Pedra'),
    ]

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_name_response(client, user, materiais):
    client.force_login(user)
    resp = client.get(reverse('materiais:estoque_materiais'),
                      data={'search': 'diamante'})
    return resp

def test_estoque_materiais_autenticado_status_code(search_name_response):
    assert search_name_response.status_code == 200

def test_search_material_works(search_name_response):
    assertContains(search_name_response, 'Diamante')
    assertNotContains(search_name_response, 'Esmeralda')
