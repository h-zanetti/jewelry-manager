import pytest
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from pytest_django.asserts import assertContains, assertNotContains

from webdev.financeiro.models import Despesa


# Fixtures
@pytest.fixture
def despesas(db):
    return [
        # Despesas únicas
        Despesa.objects.create(data=timezone.now(), categoria='Motoboy1', valor=150, repetir=''),
        # Despesas recorrentes
        Despesa.objects.create(data=timezone.now() - relativedelta(months=5),
                               categoria='MEI', valor=65, repetir='m'),
        Despesa.objects.create(data=timezone.now() - relativedelta(years=1),
                               categoria='Dominio2', valor=59.99, repetir='a'),
        # Despesas finalizadas
        Despesa.objects.create(data=timezone.now() - relativedelta(months=1),
                               categoria='Motoboy2', valor=75, repetir=''),
        Despesa.objects.create(data=timezone.now() - relativedelta(years=1),
                               categoria='Aluguel', valor=1500, repetir='m',
                               data_de_encerramento=timezone.now() - relativedelta(months=1)),
        Despesa.objects.create(data=timezone.now() - relativedelta(years=5),
                               categoria='Dominio1', valor=59.99, repetir='a',
                               data_de_encerramento=timezone.now() - relativedelta(years=1, months=1)),
    ]

@pytest.fixture
def permissionless_user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    permissions = Permission.objects.filter(content_type__app_label='financeiro', content_type__model='despesa')
    user.user_permissions.set(permissions)
    return user


# Test permissions
@pytest.fixture
def permissionless_user_response(client, permissionless_user):
    client.force_login(permissionless_user)
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_permissionless_response(permissionless_user_response):
    assert permissionless_user_response.status_code == 403


# Test GET VIEW Despesa
@pytest.fixture
def resposta_despesas(client, despesas, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_despesas_status_code(resposta_despesas):
    assert resposta_despesas.status_code == 200

def test_despesas_presente(resposta_despesas, despesas):
    for despesa in despesas[:2]:
        assertContains(resposta_despesas, despesa.categoria)
    for despesa in despesas[3:]:
        assertNotContains(resposta_despesas, despesa.categoria)

def test_despesa_plot_data_accuracy(resposta_despesas, despesas):
    data = [
        round(float(sum([despesas[4].valor])), 2),
        round(float(sum([despesas[1].valor, despesas[4].valor])), 2),
        round(float(sum([despesas[1].valor, despesas[4].valor])), 2),
        round(float(sum([despesas[1].valor, despesas[4].valor])), 2),
        round(float(sum([despesas[1].valor, despesas[4].valor])), 2),
        round(float(sum([despesas[1].valor, despesas[3].valor, despesas[4].valor])), 2),
        round(float(sum([despesas[0].valor, despesas[1].valor, despesas[2].valor])), 2),
        round(float(sum([despesas[1].valor])), 2),
        round(float(sum([despesas[1].valor])), 2),
        round(float(sum([despesas[1].valor])), 2),
        round(float(sum([despesas[1].valor])), 2),
        round(float(sum([despesas[1].valor])), 2),
    ]
    assertContains(resposta_despesas, f'data: {data}')

def test_btn_nova_despesa_presente(resposta_despesas):
    assertContains(
        resposta_despesas,
        f'href="{reverse("financeiro:nova_despesa")}'
    )


# Test GET CREATE Despesa
@pytest.fixture
def resposta_nova_despesa(client, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:nova_despesa'))
    return resp

def test_nova_despesa_status_code(resposta_nova_despesa):
    assert resposta_nova_despesa.status_code == 200

def test_create_form_present(resposta_nova_despesa):
    # pathname = reverse('financeiro:nova_despesa')
    assertContains(resposta_nova_despesa, f'<form')

def test_btn_submit_create(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<button type="submit"')


# Test GET EDIT Despesa
@pytest.fixture
def resposta_editar_despesa(client, despesas, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesas[0].id}))
    return resp

def test_editar_despesa_status_code(resposta_editar_despesa):
    assert resposta_editar_despesa.status_code == 200

def test_edit_form_present(resposta_editar_despesa, despesas):
    # pathname = reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesas[0].id})
    assertContains(resposta_editar_despesa, f'<form')


def test_btn_submit_edit(resposta_editar_despesa):
    assertContains(resposta_editar_despesa, f'<button type="submit"')
