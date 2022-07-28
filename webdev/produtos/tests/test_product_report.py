import os
import pytest
from django.urls import reverse
from webdev.produtos.models import Produto
from django.contrib.auth.models import User
from webdev.settings.base import BASE_DIR


@pytest.fixture
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')


@pytest.fixture
def product_report_response(client, product, user):
    client.force_login(user)
    resp = client.post(reverse('produtos:product_report'))
    return resp

def test_product_report_status_code(product_report_response):
    assert product_report_response.status_code == 200

