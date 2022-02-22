import os
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains
from webdev.produtos.models import Produto

# Botões presentes (GET)
@pytest.fixture
def resposta_produtos(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_btn_exportar_produtos_presente(resposta_produtos):
    assertContains(resposta_produtos, f'href="{reverse("produtos:exportar_produtos")}')

def test_btn_importar_produtos_presente(resposta_produtos):
    assertContains(resposta_produtos, f'href="{reverse("produtos:importar_produtos")}')

# Importação de produtos (POST)
@pytest.fixture
def resposta_importar_produtos(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    with open(os.path.join(os.path.dirname(__file__), 'importacoes/produtos.xlsx'), 'rb') as xl_file:
        resp = client.post(
            reverse('produtos:importar_produtos'),
            data={'myfile': xl_file}
        )
        xl_file.close()
    return resp

def test_status_code(resposta_importar_produtos):
    assert resposta_importar_produtos.status_code == 302

def test_produto_importado(resposta_importar_produtos):
    assert Produto.objects.exists()