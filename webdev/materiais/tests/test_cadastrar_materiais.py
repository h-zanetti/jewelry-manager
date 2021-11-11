import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material

# Cadastro de materiais (GET)
@pytest.fixture
def resposta_form_de_cadastro(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
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
def resposta_cadastrar_material(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:cadastrar_material'), data={
        'nome': 'Esmeralda',
        'categoria': 'Pedra',
    })
    return resp

# def test_form_sem_erros(resposta_cadastrar_material):
#     assert not resposta_cadastrar_material.context['form'].errors

def test_cadastrar_material_status_code(resposta_cadastrar_material):
    assertRedirects(resposta_cadastrar_material, reverse('materiais:estoque_materiais'))

def test_material_no_bd(resposta_cadastrar_material):
    assert Material.objects.exists()

# Estoque de matéria prima (GET)
@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
    )

@pytest.fixture
def resposta_estoque(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:estoque_materiais'))
    return resp


def test_estoque_de_materiais_status_code(resposta_estoque):
    assert resposta_estoque.status_code == 200

def test_material_presente(resposta_estoque, material):
    assertContains(resposta_estoque, material.nome)
