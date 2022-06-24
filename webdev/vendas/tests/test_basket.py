import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.produtos.models import Produto
from webdev.vendas.models import Basket, BasketItem

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def basket(db):
    return Basket.objects.create()

@pytest.fixture
def basket_item(basket, product):
    return BasketItem.objects.create(
        basket=basket,
        product=product,
        quantity=2,
    )

# GET
@pytest.fixture
def resposta_basket_summary(client, user, basket, basket_item, product):
    client.force_login(user)
    resp = client.get(reverse('vendas:basket_summary'))
    return resp

def test_basket_summary_status_code(resposta_basket_summary):
    assert resposta_basket_summary.status_code == 200

def test_item_formset_present(resposta_basket_summary):
    assertContains(resposta_basket_summary, '<input type="hidden" name="item-TOTAL_FORMS"')

def test_items_present(resposta_basket_summary, product):
    assertContains(resposta_basket_summary, f'<option value="{product.id}" selected>{product.nome}</option>')
    

@pytest.fixture
def product1(db):
    return Produto.objects.create(
        nome='Produto Mais Legal',
        colecao="d'Mentira",
    )


# POST
@pytest.fixture
def resposta_basket_add(client, user, basket, basket_item, product, product1):
    client.force_login(user)
    resp = client.post(reverse('vendas:resposta_basket_add'), data={
        'markup': 2.5,
        'item-TOTAL_FORMS': 2,
        'item-INITIAL_FORMS': 1,
        'item-0-basket': basket.id,
        'item-0-product': product.id,
        'item-0-quantity': 1,
        'item-1-basket': basket.id,
        'item-1-product': product1.id,
        'item-1-quantity': 2,
    })
    return resp

def test_resposta_basket_add_status_code(resposta_resposta_basket_add):
    assert resposta_resposta_basket_add.status_code == 302

def test_basket_item_updated(resposta_basket_add):
    assert BasketItem.objects.first() == 1

def test_basket_item_created(resposta_basket_add):
    assert len(BasketItem.objects.all()) == 2