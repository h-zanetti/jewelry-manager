from django.utils import timezone
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains
from webdev.produtos.models import Produto

@pytest.fixture
def produto(db):
    return Produto.objects.create(
        nome='Produto1',
        colecao="d'Mentira",
        observacao="Essa é uma observação do produto."
    )

# GET
@pytest.fixture
def resposta_produtos(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_btn_exportar_produtos_presente(resposta_produtos):
    assertContains(resposta_produtos, f'href="{reverse("produtos:exportar_produtos")}')

def test_btn_importar_produtos_presente(resposta_produtos):
    assertContains(resposta_produtos, f'href="{reverse("produtos:importar_produtos")}')