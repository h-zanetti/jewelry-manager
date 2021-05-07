import pytest
from django.urls import reverse
from webdev.produtos.models import Produto, Categoria
from django.contrib.auth.models import User

@pytest.fixture
def produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def resposta_editar_produto(client, produto):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:editar_produto', kwargs={'produto_id': produto.id}),
        data={
            'foto': produto.foto.url,
            'nome': 'Novo Nome',
            'colecao': produto.colecao,
            'unidades': produto.unidades,
        }
    )
    return resp

def test_editar_produto_status_code(resposta_editar_produto):
    assert resposta_editar_produto.status_code == 302

def test_editar_produto(resposta_editar_produto):
    assert Produto.objects.first().nome == 'Novo Nome'
