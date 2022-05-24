import pytest
from django.urls import reverse
from django.utils import timezone
from webdev.financeiro.models import Despesa
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User, Permission

@pytest.fixture
def despesa(db):
    return Despesa.objects.create(
        data=timezone.now(),
        categoria='Motoboy',
        valor=150,
        repetir='n'
    )

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    permissions = Permission.objects.filter(content_type__app_label='financeiro', content_type__model='despesa')
    user.user_permissions.set(permissions)
    return user


# GET
@pytest.fixture
def resposta_despesas(client, despesa, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_btn_exportar_despesas_presente(resposta_despesas):
    assertContains(resposta_despesas, f'href="{reverse("financeiro:exportar_despesas")}')

def test_btn_importar_despesas_presente(resposta_despesas):
    assertContains(resposta_despesas, f'href="{reverse("financeiro:importar_despesas")}')
