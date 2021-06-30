import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains
from webdev.materiais.models import Material

@pytest.fixture
def material(db):
    return Material.objects.create(
        unidades_compradas=3,
        valor=1000,
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        estoque=3,
    )

# GET
@pytest.fixture
def resposta_estoque(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:estoque_materiais'))
    return resp

def test_btn_exportar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:exportar_materiais")}')

def test_btn_importar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:importar_materiais")}')
