from django.utils import timezone
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains
from webdev.financeiro.models import Despesa

@pytest.fixture
def despesa(db):
    return Despesa.objects.create(
        data=timezone.now(),
        categoria='Motoboy',
        valor=150,
        repetir='n'
    )

# GET
@pytest.fixture
def resposta_despesas(client, despesa):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_btn_exportar_despesas_presente(resposta_despesas):
    assertContains(resposta_despesas, f'href="{reverse("financeiro:exportar_despesas")}')

def test_btn_importar_despesas_presente(resposta_despesas):
    assertContains(resposta_despesas, f'href="{reverse("financeiro:importar_despesas")}')
