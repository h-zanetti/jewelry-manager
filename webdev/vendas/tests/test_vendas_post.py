import pytest
from django.urls import reverse
from django.utils import timezone
from webdev.vendas.models import Venda
from webdev.produtos.models import Produto
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from webdev.financeiro.models import Parcela, Receita

@pytest.fixture
def product(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

# Nova Venda
@pytest.fixture
def resposta_nova_venda(client, product):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('vendas:nova_venda'),
        data={
            'data': timezone.localdate().strftime('%d-%m-%Y'),
            'cliente': '',
            'observacao': '',
            'valor': 4500,
            'receita': '',
            'parcelas': 12,
        }
    )
    return resp

# def test_new_sale_form_errors(resposta_nova_venda):
#     assert not resposta_nova_venda.context['form'].errors

def test_nova_venda_status_code(resposta_nova_venda):
    assert resposta_nova_venda.status_code == 302

def test_nova_venda_criada(resposta_nova_venda):
    assert Venda.objects.exists()

def test_receita_criada(resposta_nova_venda):
    assert Receita.objects.exists()

def test_parcelas_criadas(resposta_nova_venda):
    venda = Venda.objects.first()
    for parcela in range(venda.parcelas):
        assert Parcela.objects.get(
            data=timezone.localdate() + relativedelta(months=parcela),
            valor=venda.get_valor_parcela()
        ) != None

# Editar Venda
@pytest.fixture
def venda(db):
    venda = Venda.objects.create(
        data=timezone.now(),
        parcelas=6,
        valor=1200
    )
    return venda

@pytest.fixture
def resposta_editar_venda(client, venda):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('vendas:editar_venda', kwargs={'venda_id': venda.id}),
        data={
            'data': timezone.localdate().strftime('%d/%m/%Y'),
            'cliente': '',
            'observacao': '',
            'valor': 12000,
            'receita': venda.receita.id,
            'parcelas': 12,
        }
    )
    return resp

def test_editar_venda_status_code(resposta_editar_venda):
    assert resposta_editar_venda.status_code == 302

def test_venda_alterada(resposta_editar_venda):
    venda = Venda.objects.first()
    assert venda.parcelas == 12

def test_parcelas_alteradas(resposta_editar_venda, venda):
    for parcela in range(venda.parcelas):
        assert Parcela.objects.get(
            data=timezone.localdate() + relativedelta(months=parcela),
            valor=1000
        ) != None

# Deletar Venda
@pytest.fixture
def resposta_deletar_venda(client, venda):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('vendas:deletar_venda', kwargs={'venda_id': venda.id}))
    return resp

def test_deletar_despesa_status_code(resposta_deletar_venda):
    assert resposta_deletar_venda.status_code == 302

def test_despesa_deletada(resposta_deletar_venda):
    assert not Venda.objects.exists()

def test_receita_deletada(resposta_deletar_venda):
    assert not Receita.objects.exists()

def test_parcelas_deletadas(resposta_deletar_venda):
    assert not Parcela.objects.exists()

