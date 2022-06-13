import pytest
import datetime as dt
from django.urls import reverse
from webdev.vendas.models import Venda
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def sales(db):
    return [
        Venda.objects.create(data=dt.date(2020, 1, 1), valor=1000, parcelas=1),
        Venda.objects.create(data=dt.date(2020, 3, 1), valor=5000, parcelas=1),
    ]

@pytest.fixture
def sorted_sales_response(client, user, sales):
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
