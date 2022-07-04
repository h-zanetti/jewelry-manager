import pytest
import datetime as dt
from django.urls import reverse
from webdev.produtos.models import Produto
from webdev.vendas.models import Venda, Basket, BasketItem, MarkUp
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def markups(db):
    return [
        MarkUp.objects.create(key='Cliente final', value=3),
        MarkUp.objects.create(key='Atacado', value=1.75),
    ]

@pytest.fixture
def baskets(markups):
    return [
        Basket.objects.create(markup=markups[0]),
        Basket.objects.create(markup=markups[1]),
    ]

@pytest.fixture
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def basket_items(baskets, product):
    return [
        BasketItem.objects.create(basket=baskets[0], product=product, quantity=2),
        BasketItem.objects.create(basket=baskets[1], product=product, quantity=1),
    ]

@pytest.fixture
def sales(baskets):
    return [
        Venda.objects.create(data=dt.date(2020, 1, 1), valor=2000, parcelas=1, basket=baskets[0]),
        Venda.objects.create(data=dt.date(2020, 3, 1), valor=1000, parcelas=1, basket=baskets[1]),
    ]

@pytest.fixture
def sorted_sales_response(client, user, baskets, basket_items, sales):
    client.force_login(user)
    resp = client.get(reverse('vendas:minhas_vendas'), data={
        'sort-field': 'data',
        'sort-order': '-',
    })
    return resp

def test_sorted_clients_status_code(sorted_sales_response):
    assert sorted_sales_response.status_code == 200

def test_clients_sorted(sorted_sales_response, sales):
    assert sorted_sales_response.context['vendas'][0] == sales[1]
