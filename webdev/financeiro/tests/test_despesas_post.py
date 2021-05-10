import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.financeiro.models import Despesa
from django.utils import timezone

# Nova Despesa
@pytest.fixture
def resposta_nova_despesa(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('financeiro:nova_despesa'),
        data={
            'data': '26-04-2021',
            'categoria': 'Motoboy',
            'total_pago': 150,
            'repetir': 'n'
        }
    )
    return resp

def test_despesas_status_code(resposta_nova_despesa):
    assert resposta_nova_despesa.status_code == 302

def test_nova_despesa_criada(resposta_nova_despesa):
    assert Despesa.objects.exists()

# Editar Despesas
@pytest.fixture
def despesa(db):
    return Despesa.objects.create(data=timezone.now(), categoria='Motoboy', total_pago=150, repetir='n')

@pytest.fixture
def resposta_editar_despesa(client, despesa):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesa.id}),
        data={
            'data': '26-04-2021',
            'categoria': 'Manutenção',
            'total_pago': 150,
            'repetir': 'n'
        }
    )
    return resp

def test_editar_despesa_status_code(resposta_editar_despesa):
    assert resposta_editar_despesa.status_code == 302

def test_despesa_editada(resposta_editar_despesa):
    assert Despesa.objects.first().categoria == 'Manutenção'

# Deletar Despesa
@pytest.fixture
def resposta_deletar_despesa(client, despesa):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('financeiro:deletar_despesa', kwargs={'despesa_id': despesa.id}))
    return resp

def test_deletar_despesa_status_code(resposta_deletar_despesa):
    assert resposta_deletar_despesa.status_code == 302

def test_despesa_deletada(resposta_deletar_despesa):
    assert not Despesa.objects.exists()

