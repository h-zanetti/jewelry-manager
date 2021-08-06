import os
from webdev.financeiro.models import Despesa
import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material

@pytest.fixture
def resposta_entradas(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:entradas_de_materiais'))
    return resp

def test_btn_exportar_materiais_presente(resposta_entradas):
    assertContains(resposta_entradas, f'href="{reverse("materiais:exportar_entradas")}')

def test_btn_importar_materiais_presente(resposta_entradas):
    assertContains(resposta_entradas, f'href="{reverse("materiais:importar_entradas")}')

# Importação de materiais (POST)
@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
    )

@pytest.fixture
def resposta_importar_entradas(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    with open(os.path.join(os.path.dirname(__file__), 'importacoes/entradas.xls'), 'rb') as xl_file:
        resp = client.post(
            reverse('materiais:importar_entradas'),
            data={'myfile': xl_file}
        )
        xl_file.close()
    return resp

def test_status_code(resposta_importar_entradas):
    assert resposta_importar_entradas.status_code == 302

def test_entrada_importada(resposta_importar_entradas):
    assert Entrada.objects.exists()

def test_despesa_criada(resposta_importar_entradas):
    assert Despesa.objects.exists()
