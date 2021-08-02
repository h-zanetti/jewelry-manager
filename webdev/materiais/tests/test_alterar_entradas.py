import datetime as dt
from webdev.financeiro.models import Despesa
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Fornecedor

# Editar entrada
@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
    )

@pytest.fixture
def entrada(material):
    return Entrada.objects.create(
        material=material,
        data='2021-04-26',
        unidades=3,
        peso=0.17,
        unidade_de_medida='ct',
        valor=1000
    )

@pytest.fixture
def resposta_form_editar_entrada(client, entrada):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    return client.get(
        reverse('materiais:editar_entrada',
        kwargs={'entrada_id': entrada.id})
    )

def test_form_editar_entrada_status_code(resposta_form_editar_entrada):
    assert resposta_form_editar_entrada.status_code == 200

def test_despesa_criada(resposta_form_editar_entrada):
    assert Despesa.objects.exists()
    assert Despesa.objects.first().valor == 1000

@pytest.fixture
def resposta_editar_entrada(client, entrada, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('materiais:editar_entrada', kwargs={'entrada_id': entrada.id}),
        data={
            'data': '2021-05-26',
            'material': material.id,
            'despesa': entrada.despesa.id,
            'unidades': 3,
            'peso': 0.17,
            'unidade_de_medida': 'ct',
            'valor': 1500,
        }
    )
    return resp

# def test_form_sem_erros(resposta_editar_entrada):
#     assert not resposta_editar_entrada.context['form'].errors

def test_editar_entrada_status_code(resposta_editar_entrada):
    assert resposta_editar_entrada.status_code == 302

def test_entrada_alterada(resposta_editar_entrada):
    assert Entrada.objects.first().valor == 1500
    assert Entrada.objects.first().data == dt.date(2021, 5, 26)

def test_despesa_alterada(resposta_editar_entrada):
    assert Despesa.objects.first().valor == 1500
    assert Despesa.objects.first().data == dt.date(2021, 5, 26)

# Deletar Entrada
@pytest.fixture
def resposta_deletar_entrada(client, entrada):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    return client.post(
        reverse('materiais:deletar_entrada',
        kwargs={'entrada_id': entrada.id})
    )

def test_deletar_entrada_status_code(resposta_deletar_entrada):
    assert resposta_deletar_entrada.status_code == 302

def test_entrada_deletada(resposta_deletar_entrada):
    assert not Entrada.objects.exists()

def test_despesa_deletada(resposta_deletar_entrada):
    assert not Despesa.objects.exists()
