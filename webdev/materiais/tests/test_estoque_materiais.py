import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from pytest_django.asserts import assertContains

@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
    )

# Estoque de matéria prima
@pytest.fixture
def resposta_estoque(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:estoque_materiais'))
    return resp

def test_estoque_materiais_status_code(resposta_estoque):
    assert resposta_estoque.status_code == 200

def test_materiais_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'{material.nome}')

def test_btn_estoque_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:estoque_materiais")}"')

def test_btn_nova_entrada_presente(resposta_estoque):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:entrada_de_material")}"')

def test_btn_editar_material_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:editar_material", kwargs={"material_id": material.id})}"')

def test_btn_deletar_material_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'<form action="{reverse("materiais:deletar_material", kwargs={"material_id": material.id})}"')

def test_btn_exportar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:exportar_materiais")}')

def test_btn_importar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:importar_materiais")}')
