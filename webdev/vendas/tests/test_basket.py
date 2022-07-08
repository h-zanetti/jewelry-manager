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
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def markups(db):
    return [
        MarkUp.objects.create(key='Cliente final', value=3),
        MarkUp.objects.create(key='Atacado', value=1.75),
    ]

@pytest.fixture
def basket(markups):
    return Basket.objects.create(markup=markups[0])

@pytest.fixture
def basket_item(basket, product):
    return BasketItem.objects.create(
        basket=basket,
        product=product,
        quantity=2,
    )

# GET Basket Summary
@pytest.fixture
def resposta_basket_summary(client, user, basket, basket_item, product, markups):
    client.force_login(user)
    resp = client.get(reverse('vendas:basket_summary'))
    return resp

def test_basket_summary_status_code(resposta_basket_summary):
    assert resposta_basket_summary.status_code == 200

def test_markups_present(resposta_basket_summary, markups):
    for markup in markups:
        selected = ''
        if markup == markups[0]:
            selected = ' selected'
        assertContains(resposta_basket_summary, f'<option value="{markup.id}"' + selected + f'>{markup.key}</option>')

def test_item_form_present(resposta_basket_summary, basket):
    assertContains(resposta_basket_summary, f'<input type="hidden" name="item-basket" value="{basket.id}" disabled id="id_item-basket">')

def test_basket_review_btn_present(resposta_basket_summary):
    assertContains(resposta_basket_summary, f'<a href="{reverse("vendas:basket_review")}"')

def test_bitem_present(resposta_basket_summary, product):
    assertContains(resposta_basket_summary, f'<td>{product.nome}</td>')

def test_delete_bitem_present(resposta_basket_summary, product):
    assertContains(
        resposta_basket_summary,
        f'<form action="{reverse("vendas:basket_remove", kwargs={"pk": product.pk})}" method="POST">')


# GET Basket Review
@pytest.fixture
def resposta_basket_review(client, user, basket, basket_item, markups):
    client.force_login(user)
    resp = client.get(reverse('vendas:basket_review'))
    return resp

def test_basket_review_status_code(resposta_basket_review):
    assert resposta_basket_review.status_code == 200

def test_assert_bitem_present(resposta_basket_review, basket_item):
    assertContains(resposta_basket_review, basket_item.product.nome)
    assertContains(resposta_basket_review, basket_item.quantity)



@pytest.fixture
def product1(db):
    return Produto.objects.create(
        nome='Produto Mais Legal',
        colecao="d'Mentira",
    )

# POST Basket summary
@pytest.fixture
def resposta_post_basket_summary(client, user, product, product1, basket, basket_item, markups):
    client.force_login(user)
    resp = client.post(reverse('vendas:basket_summary'), data={
        'basket-markup': markups[0].id,
        'item-basket': basket.id,
        'item-product': product1.get_barcode_obj().get_fullcode(),
        'item-quantity': 2,
    })
    return resp

# def test_basket_summary_item_form_errors(resposta_post_basket_summary):
#     assert not resposta_post_basket_summary.context['basket_form'].errors
#     assert not resposta_post_basket_summary.context['item_form'].errors

def test_resposta_basket_summary_status_code(resposta_post_basket_summary):
    assert resposta_post_basket_summary.status_code == 302

def test_basket_item_created(resposta_post_basket_summary):
    assert len(BasketItem.objects.all()) == 2

def test_basket_still_active(resposta_post_basket_summary, basket):
    assert basket.is_active


# POST Basket remove
@pytest.fixture
def resposta_basket_remove(client, user, basket_item):
    client.force_login(user)
    return client.post(reverse('vendas:basket_remove', kwargs={'pk': basket_item.pk}))


def test_resposta_basket_remove_status_code(resposta_basket_remove):
    assert resposta_basket_remove.status_code == 302

def test_basket_item_removed(resposta_basket_remove):
    assert not BasketItem.objects.exists()


# POST Basket review
@pytest.fixture
def resposta_post_basket_review(client, user, product, product1, basket, basket_item, markups):
    client.force_login(user)
    resp = client.post(reverse('vendas:basket_review'), data={
        'data': '07-07-2022',
        'basket': basket.id,
        'valor': 1500,
        'parcelas': 1,
    })
    return resp


# def test_basket_review_form_errors(resposta_post_basket_review):
#     assert not resposta_post_basket_review.context['form'].errors

def test_resposta_basket_summary_redirection(resposta_post_basket_review):
    assertRedirects(resposta_post_basket_review, reverse('vendas:minhas_vendas'))

def test_sale_created(resposta_post_basket_review):
    assert Venda.objects.exists()

def test_receita_created(resposta_post_basket_review):
    assert Receita.objects.exists()