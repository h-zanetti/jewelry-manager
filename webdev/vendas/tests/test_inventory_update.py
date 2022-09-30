import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains, assertRedirects

from webdev.produtos.models import Produto
from webdev.financeiro.models import Receita
from webdev.vendas.models import Basket, BasketItem, MarkUp, Venda


@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def products(db):
    return [
        Produto.objects.create(nome='Produto legal',colecao="d'Mentira",unidades=2),
        Produto.objects.create(nome='Produto mais legal',colecao="d'Mentira",unidades=2),
        Produto.objects.create(nome='Produto nada legal',colecao="d'Mentira",unidades=0),
    ]

@pytest.fixture
def markup(db):
    return MarkUp.objects.create(key='Cliente final', value=3)

@pytest.fixture
def basket(markup):
    return Basket.objects.create(markup=markup)

@pytest.fixture
def basket_items(basket, products):
    return [ 
        BasketItem.objects.create(basket=basket,product=p,quantity=2) \
        for p in products
    ]


@pytest.fixture
def invalid_basket_review_response(client, user, products, markup, basket, basket_items):
    client.force_login(user)
    resp = client.post(reverse('vendas:basket_review'), data={
        'data': '07-07-2022',
        'basket': basket.id,
        'valor': 1500,
        'parcelas': 1,
        'update_inventory': True,
    })
    return resp

def test_insuficient_inventory_redirection(invalid_basket_review_response):
    assertRedirects(invalid_basket_review_response, reverse('vendas:basket_summary'))

def test_nova_venda_criada(invalid_basket_review_response):
    assert not Venda.objects.exists()

def test_receita_created(invalid_basket_review_response):
    assert not Receita.objects.exists()

def test_basket_is_active(invalid_basket_review_response):
    assert Basket.objects.filter(is_active=True)

def test_inventory_is_intanct(invalid_basket_review_response):
    for p in Produto.objects.all():
        assert p.unidades == p.unidades


@pytest.fixture
def basket_items2(basket, products):
    return [ 
        BasketItem.objects.create(basket=basket,product=p,quantity=2) \
        for p in products if p.unidades >= 2
    ]


@pytest.fixture
def basket_review_response(client, user, products, markup, basket, basket_items2):
    client.force_login(user)
    resp = client.post(reverse('vendas:basket_review'), data={
        'data': '07-07-2022',
        'basket': basket.id,
        'valor': 1500,
        'parcelas': 1,
        'update_inventory': True,
    })
    return resp

def test_new_sale_redirection(basket_review_response):
    assertRedirects(basket_review_response, reverse('vendas:minhas_vendas'))

def test_new_sale_exists(basket_review_response):
    assert Venda.objects.exists()

def test_revenue_exists(basket_review_response):
    assert Receita.objects.exists()

def test_basket_is_closed(basket_review_response):
    assert Basket.objects.filter(is_active=False)

def test_inventory_is_updated(basket_review_response):
    for p in Produto.objects.all():
        assert p.unidades == 0
