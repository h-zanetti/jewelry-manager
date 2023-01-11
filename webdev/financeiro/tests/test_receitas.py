from dateutil.relativedelta import relativedelta
import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains
from webdev.financeiro.models import Receita, Parcela

# Receita
@pytest.fixture
def receita(db):
    return Receita.objects.create(categoria='Venda')

# Parcelas
@pytest.fixture
def lista_de_parcelas(receita):
    parcelas = []
    for i in range(7):
        parcela = Parcela.objects.create(
            data=timezone.now() + relativedelta(months=i),
            valor=150,
            receita=receita
        )
        parcelas.append(parcela)
    return parcelas

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    permissions = Permission.objects.filter(content_type__app_label='financeiro', content_type__model='receita')
    user.user_permissions.set(permissions)
    return user

# Visualizar receita
@pytest.fixture
def resposta_receita(client, receita, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:receitas'))
    return resp

def test_receita_status_code(resposta_receita):
    assert resposta_receita.status_code == 200

def test_receita_presente(resposta_receita, receita):
    assertContains(resposta_receita, receita.categoria)

# def test_btn_editar_receita_presente(resposta_receita, receita):
#     assertContains(resposta_receita, f'<a href="{reverse("financeiro:editar_receita", kwargs={"receita_id": receita.id})}')

# def test_btn_deletar_receita_presente(resposta_receita, receita):
#     assertContains(resposta_receita, f'<form action="{reverse("financeiro:deletar_receita", kwargs={"receita_id": receita.id})}')

# Novas receita
@pytest.fixture
def resposta_nova_receita(client, user):
    client.force_login(user)
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

# Editar receita
@pytest.fixture
def resposta_editar_receita(client, receita, user):
    client.force_login(user)
    resp = client.get(reverse('financeiro:editar_receita', kwargs={'receita_id': receita.id}))
    return resp

def test_editar_receita_status_code(resposta_editar_receita):
    assert resposta_editar_receita.status_code == 200

def test_form_editar_receita_presente(resposta_editar_receita):
    assertContains(resposta_editar_receita, f'<form')

def test_btn_submit_stay_nao_presente(resposta_editar_receita):
    assertNotContains(resposta_editar_receita, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_editar_receita):
    assertContains(resposta_editar_receita, f'<button type="submit" name="submit-leave"')


# Deletar receita
@pytest.fixture
def resposta_deletar_receita(client, receita, user):
    client.force_login(user)
    resp = client.post(reverse('financeiro:deletar_receita', kwargs={'receita_id': receita.id}))
    return resp

def test_deletar_receita_status_code(resposta_deletar_receita):
    assert resposta_deletar_receita.status_code == 302

def test_receita_deletada(resposta_deletar_receita):
    assert not Receita.objects.exists()
