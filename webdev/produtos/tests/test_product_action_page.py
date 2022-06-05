import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.produtos.models import Produto
from pytest_django.asserts import assertContains

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def produtos(db):
    return [
        Produto.objects.create(nome='Produto1', colecao='Pedra'),
        Produto.objects.create(nome='Produto2', colecao='Pedra'),
        Produto.objects.create(nome='Produto3', colecao='Metal'),
        Produto.objects.create(nome='Produto4', colecao='Metal'),
    ]

# GET action page
@pytest.fixture
def action_page_get_response(client, user, produtos):
    client.force_login(user)
    resp = client.get(reverse('produtos:product_actions'))
    return resp

def test_action_page_status_code(action_page_get_response):
    assert action_page_get_response.status_code == 200

def test_form_present(action_page_get_response):
    assertContains(action_page_get_response, f'<form')

def test_submit_btn_present(action_page_get_response):
    assertContains(action_page_get_response, '<button type="submit"')

def test_all_produtos_present(action_page_get_response, produtos):
    for produto in produtos:
        assertContains(action_page_get_response, produto.nome)
