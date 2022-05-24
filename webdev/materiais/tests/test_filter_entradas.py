import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains
from webdev.materiais.models import Material, Entrada
from django.contrib.auth.models import User

@pytest.fixture
def materiais(db):
    return [
        Material.objects.create(nome='Diamante', categoria='Pedra'),
        Material.objects.create(nome='Esmeralda', categoria='Pedra'),
    ]

@pytest.fixture
def entradas(materiais):
    return [
        Entrada.objects.create(material=materiais[0], data='2021-04-26',
                                unidades=3, peso=0.17,
                                unidade_de_medida='ct', valor=1000),
        Entrada.objects.create(material=materiais[1], data='2021-06-26',
                                unidades=4, peso=0.21,
                                unidade_de_medida='ct', valor=1500),
    ]
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_entrada_response(client, user, materiais, entradas):
    client.force_login(user)
    resp = client.get(reverse('materiais:entradas_de_materiais'),
                      data={'search': 'diamante'})
    return resp

def test_entradas_status_code(search_entrada_response):
    assert search_entrada_response.status_code == 200

def test_search_entradas_works(search_entrada_response):
    assertContains(search_entrada_response, 'Diamante')
    assertNotContains(search_entrada_response, 'Esmeralda')
