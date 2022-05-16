import pytest
from django.urls import reverse
from webdev.materiais.models import Material, Entrada
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def materiais(db):
    return [
        Material.objects.create(nome='Material1', categoria="d'Mentira"),
        Material.objects.create(nome='Material2', categoria="d'Mentira")
    ]

@pytest.fixture
def resposta_sorted_materials(client, user, materiais):
    client.force_login(user)
    resp = client.get(reverse('materiais:estoque_materiais'), data={
        'sort-field': 'nome',
        'sort-order': '-',
    })
    return resp

def test_sorted_materials_status_code(resposta_sorted_materials):
    assert resposta_sorted_materials.status_code == 200

def test_materials_sorted(resposta_sorted_materials):
    assert resposta_sorted_materials.context['materiais'][0].nome == 'Material2'
