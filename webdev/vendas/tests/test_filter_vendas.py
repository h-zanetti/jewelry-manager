import pytest
import datetime as dt
from django.urls import reverse
from webdev.vendas.models import Venda
from django.contrib.auth.models import User

@pytest.fixture
def sales(db):
    return [
        Venda.objects.create(data=dt.date(2020, 1, 1), valor=1000, parcelas=1),
        Venda.objects.create(data=dt.date(2020, 3, 1), valor=5000, parcelas=1),
    ]

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def search_date_response(client, user, sales):
    client.force_login(user)
    resp = client.get(reverse('vendas:minhas_vendas'),
                      data={'search': '2020-01-01'})
    return resp

def test_filtered_sales_status_code(search_date_response):
    assert search_date_response.status_code == 200

def test_search_sale_works(search_date_response, sales):
    assert sales[0] in search_date_response.context['vendas']
    assert sales[1] not in search_date_response.context['vendas']
    