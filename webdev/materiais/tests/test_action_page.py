import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from pytest_django.asserts import assertContains, assertRedirects

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def materiais(db):
    return [
        Material.objects.create(nome='Esmeralda',categoria='Pedra'),
        Material.objects.create(nome='Diamante',categoria='Pedra'),
        Material.objects.create(nome='Prata',categoria='Metal'),
        Material.objects.create(nome='Ouro',categoria='Metal'),
    ]

# GET action page
@pytest.fixture
def action_page_get_response(client, user, materiais):
    client.force_login(user)
    resp = client.get(reverse('materiais:material_actions'))
    return resp

def test_action_page_status_code(action_page_get_response):
    assert action_page_get_response.status_code == 200

def test_form_present(action_page_get_response):
    assertContains(action_page_get_response, f'<form')

def test_submit_btn_present(action_page_get_response):
    assertContains(action_page_get_response, '<button type="submit"')

def test_all_materials_present(action_page_get_response, materiais):
    for material in materiais:
        assertContains(action_page_get_response, material.nome)
