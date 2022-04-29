import pytest
from django.urls import reverse
from django.utils import timezone
from webdev.financeiro.models import Despesa
from django.contrib.auth.models import User, Permission
from pytest_django.asserts import assertContains, assertNotContains

# Fixtures
@pytest.fixture
def despesas(db):
    return [
        Despesa.objects.create(data=timezone.now(), categoria='Motoboy', valor=150, repetir='n'),
        Despesa.objects.create(data=timezone.now(), categoria='MEI', valor=65, repetir='m')
    ]

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    permissions = Permission.objects.filter(content_type__app_label='financeiro', content_type__model='despesa')
    user.user_permissions.set(permissions)
    return user

# Visualizar Despesas
@pytest.fixture
def resposta_despesas(client, despesas, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:despesas'))
    return resp

def test_despesas_status_code(resposta_despesas):
    assert resposta_despesas.status_code == 200

def test_despesas_presente(resposta_despesas, despesas):
    for despesa in despesas:
        assertContains(resposta_despesas, despesa.categoria)

def test_btn_nova_despesa_presente(resposta_despesas):
    assertContains(
        resposta_despesas,
        f'<a href="{reverse("financeiro:nova_despesa")}'
    )

def test_btn_entrada_de_material_presente(resposta_despesas):
    assertContains(
        resposta_despesas,
        f'<a href="{reverse("materiais:entrada_de_material")}'
    )

def test_btn_novo_servico_presente(resposta_despesas):
    assertContains(
        resposta_despesas,
        f'<a href="{reverse("fornecedores:novo_servico")}'
    )

def test_btn_editar_despesa_presente(resposta_despesas, despesas):
    for despesa in despesas:
        assertContains(resposta_despesas, f'<a href="{reverse("financeiro:editar_despesa", kwargs={"despesa_id": despesa.id})}')

def test_btn_deletar_despesa_presente(resposta_despesas, despesas):
    for despesa in despesas:
        assertContains(resposta_despesas, f'<form action="{reverse("financeiro:deletar_despesa", kwargs={"despesa_id": despesa.id})}')

# Novas Despesas
@pytest.fixture
def resposta_nova_despesa(client, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:nova_despesa'))
    return resp

def test_nova_despesa_status_code(resposta_nova_despesa):
    assert resposta_nova_despesa.status_code == 200

def test_form_presente(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<form')

def test_btn_submit_stay_presente(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_nova_despesa):
    assertContains(resposta_nova_despesa, f'<button type="submit" name="submit-leave"')

# Editar Despesas
@pytest.fixture
def resposta_editar_despesa(client, despesas, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesas[0].id}))
    return resp

def test_editar_despesa_status_code(resposta_editar_despesa):
    assert resposta_editar_despesa.status_code == 200

def test_form_editar_despesa_presente(resposta_editar_despesa):
    assertContains(resposta_editar_despesa, f'<form')

def test_btn_submit_stay_nao_presente(resposta_editar_despesa):
    assertNotContains(resposta_editar_despesa, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_editar_despesa):
    assertContains(resposta_editar_despesa, f'<button type="submit" name="submit-leave"')
