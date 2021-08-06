import os
import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material

@pytest.fixture
def resposta_estoque(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:estoque_materiais'))
    return resp

def test_btn_exportar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:exportar_materiais")}')

def test_btn_importar_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'href="{reverse("materiais:importar_materiais")}')

# Importação de materiais (POST)
@pytest.fixture
def resposta_importar_materiais(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    with open(os.path.join(os.path.dirname(__file__), 'importacoes/materiais.xls'), 'rb') as xl_file:
        resp = client.post(
            reverse('materiais:importar_materiais'),
            data={'myfile': xl_file}
        )
        xl_file.close()
    return resp

def test_status_code(resposta_importar_materiais):
    assert resposta_importar_materiais.status_code == 302

def test_material_importado(resposta_importar_materiais):
    assert Material.objects.exists()
