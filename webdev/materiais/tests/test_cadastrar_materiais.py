import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

# Cadastro de materiais (GET)
@pytest.fixture
def resposta_form_de_cadastro(client, user):
    client.force_login(user)
    resp = client.get(reverse('materiais:cadastrar_material'))
    return resp

def test_cadastrar_material_status_code(resposta_form_de_cadastro):
    assert resposta_form_de_cadastro.status_code == 200

def test_form_presente(resposta_form_de_cadastro):
    assertContains(resposta_form_de_cadastro, f'<form')

def test_btn_submit_stay_presente(resposta_form_de_cadastro):
    assertContains(resposta_form_de_cadastro, '<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_form_de_cadastro):
    assertContains(resposta_form_de_cadastro, '<button type="submit" name="submit-leave"')

# Cadastro de materiais (POST)
@pytest.fixture
def resposta_cadastrar_material(client, user):
    client.force_login(user)
    resp = client.post(reverse('materiais:cadastrar_material'), data={
        'nome': 'Esmeralda',
        'categoria': 'Pedra',
        'valor': 250,
    })
    return resp

# def test_form_sem_erros(resposta_cadastrar_material):
#     assert not resposta_cadastrar_material.context['form'].errors

def test_cadastrar_material_status_code(resposta_cadastrar_material):
    assertRedirects(resposta_cadastrar_material, reverse('materiais:estoque_materiais'))

def test_material_no_bd(resposta_cadastrar_material):
    assert Material.objects.exists()
