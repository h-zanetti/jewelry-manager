import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains
from webdev.financeiro.models import Receita

# Receitas
@pytest.fixture
def receitas(db):
    return [
        Receita.objects.create(data=timezone.now(), categoria='Motoboy', valor=150),
        Receita.objects.create(data=timezone.now(), categoria='MEI', valor=65)
    ]

# Visualizar receitas
@pytest.fixture
def resposta_receitas(client, receitas):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:receitas'))
    return resp

def test_receitas_status_code(resposta_receitas):
    assert resposta_receitas.status_code == 200

def test_receitas_presente(resposta_receitas, receitas):
    for receita in receitas:
        assertContains(resposta_receitas, receita.categoria)

def test_btn_editar_receita_presente(resposta_receitas, receitas):
    for receita in receitas:
        assertContains(resposta_receitas, f'<a href="{reverse("financeiro:editar_receita", kwargs={"receita_id": receita.id})}')

def test_btn_deletar_receita_presente(resposta_receitas, receitas):
    for receita in receitas:
        assertContains(resposta_receitas, f'<form action="{reverse("financeiro:deletar_receita", kwargs={"receita_id": receita.id})}')

# Novas Receitas
@pytest.fixture
def resposta_nova_receita(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:nova_receita'))
    return resp

def test_nova_receita_status_code(resposta_nova_receita):
    assert resposta_nova_receita.status_code == 200

def test_form_presente(resposta_nova_receita):
    assertContains(resposta_nova_receita, f'<form')

def test_btn_submit_stay_presente(resposta_nova_receita):
    assertContains(resposta_nova_receita, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_nova_receita):
    assertContains(resposta_nova_receita, f'<button type="submit" name="submit-leave"')

# Editar Receitas
@pytest.fixture
def resposta_editar_receita(client, receitas):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('financeiro:editar_receita', kwargs={'receita_id': receitas[0].id}))
    return resp

def test_editar_receita_status_code(resposta_editar_receita):
    assert resposta_editar_receita.status_code == 200

def test_form_editar_receita_presente(resposta_editar_receita):
    assertContains(resposta_editar_receita, f'<form')

def test_btn_submit_stay_nao_presente(resposta_editar_receita):
    assertNotContains(resposta_editar_receita, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_editar_receita):
    assertContains(resposta_editar_receita, f'<button type="submit" name="submit-leave"')
