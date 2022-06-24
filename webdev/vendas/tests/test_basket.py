import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.produtos.models import Produto
from webdev.vendas.models import Basket, BasketItem, Venda

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

def test_item_present(resposta_basket_summary, product):
    assertContains(resposta_basket_summary, f'<option value="{product.id}" selected>{product.nome}</option>')


@pytest.fixture
def product1(db):
    return Produto.objects.create(
        nome='Produto Mais Legal',
        colecao="d'Mentira",
    )


# POST
@pytest.fixture
def resposta_basket_add(client, user, product, product1, basket, basket_item):
    client.force_login(user)
    resp = client.post(reverse('vendas:basket_summary'), data={
        'markup': 2.5,
        'item-basket': basket.id,
        'item-product': product1.id,
        'item-quantity': 2,
    })
    return resp


# def test_basket_add_item_form_errors(resposta_basket_add):
#     assert not resposta_basket_add.context['basket_form'].errors
#     assert not resposta_basket_add.context['item_form'].errors

def test_resposta_basket_add_status_code(resposta_basket_add):
    assert resposta_basket_add.status_code == 302

def test_basket_item_created(resposta_basket_add):
    assert len(BasketItem.objects.all()) == 2

def test_basket_still_active(resposta_basket_add, basket):
    assert basket.is_active


@pytest.fixture
def resposta_basket_remove(client, user, basket_item):
    client.force_login(user)
    return client.post(reverse('vendas:basket_remove', kwargs={'pk': basket_item.pk}))


def test_resposta_basket_remove_status_code(resposta_basket_remove):
    assert resposta_basket_remove.status_code == 302

def test_basket_item_removed(resposta_basket_remove):
    assert not BasketItem.objects.exists()

