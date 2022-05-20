import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def materiais(db):
    materials =  [
        Material.objects.create(nome='Esmeralda',categoria='Pedra'),
        Material.objects.create(nome='Diamante',categoria='Pedra'),
        Material.objects.create(nome='Prata',categoria='Metal'),
        Material.objects.create(nome='Ouro',categoria='Metal'),
    ]
    return materials

# GET material barcode page
@pytest.fixture
def material_barcode_response(client, user, materiais):
    client.force_login(user)
    resp = client.get(reverse('materiais:material_barcode'), data={
        'materials': [1,2]
    })
    return resp

def test_material_barcode_status_code(material_barcode_response):
    assert material_barcode_response.status_code == 200

def test_materials_present(material_barcode_response, materiais):
    for material in materiais[:2]:
        assertContains(material_barcode_response, material.nome)

def test_materials_filtered_out(material_barcode_response, materiais):
    for material in materiais[-2:]:
        assertNotContains(material_barcode_response, material.nome)
