import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.financeiro.models import Despesa
from django.utils import timezone
from pytest_django.asserts import assertContains

# Visualizar Despesas
@pytest.fixture
def lista_de_despesas(db):
    return [
        Despesa.objects.create(data=timezone.now(), categoria='Motoboy', total_pago=150, repetir='n'),
        Despesa.objects.create(data=timezone.now(), categoria='MEI', total_pago=65, repetir='m')
    ]

@pytest.fixture
def resposta_despesas(client, lista_de_despesas):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_despesas_status_code(resposta_despesas):
    assert resposta_despesas.status_code == 200

def test_lista_de_despesas_presente(resposta_despesas, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_despesas, despesa.categoria)

def test_btn_nova_despesa_presente(resposta_despesas):
    assertContains(resposta_despesas, f'<a href="{reverse("financeiro:nova_despesa")}')

def test_btn_editar_despesa_presente(resposta_despesas, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_despesas, f'<a href="{reverse("financeiro:editar_despesa", kwargs={"despesa_id": despesa.id})}')

def test_btn_deletar_despesa_presente(resposta_despesas, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_despesas, f'<form action="{reverse("financeiro:deletar_despesa", kwargs={"despesa_id": despesa.id})}')

# Novas Despesas
@pytest.fixture
def resposta_nova_despesa(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:nova_despesa'))
    return resp

def test_nova_despesa_status_code(resposta_nova_despesa):
    assert resposta_nova_despesa.status_code == 200

def test_form_presente(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<form')

def test_btn_submit_presente(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<button type="submit"')

# Editar Despesas
@pytest.fixture
def resposta_editar_despesa(client, lista_de_despesas):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:editar_despesa', kwargs={'despesa_id': lista_de_despesas[0].id}))
    return resp

def test_editar_despesa_status_code(resposta_editar_despesa):
    assert resposta_editar_despesa.status_code == 200

def test_form_editar_despesa_presente(resposta_editar_despesa):
    assertContains(resposta_editar_despesa, f'<form')

def test_btn_submit_editar_despesa_presente(resposta_editar_despesa):
    assertContains(resposta_editar_despesa, f'<button type="submit"')
