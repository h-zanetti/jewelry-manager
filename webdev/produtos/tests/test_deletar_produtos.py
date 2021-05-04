import pytest
from django.urls import reverse
from webdev.produtos.models import Produto, Categoria
from django.contrib.auth.models import User

@pytest.fixture
def criar_produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
        familia='Zanetti',
        data_criacao='2021-04-30',
        unidades=0,
        tamanho=22
    )


@pytest.fixture
def resposta_deletar_produto(client, criar_produto):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('produtos:deletar_produto', kwargs={'produto_id': criar_produto.id}))
    return resp

def test_deletar_produto_status_code(resposta_deletar_produto):
    assert resposta_deletar_produto.status_code == 302

def test_deletar_produto(resposta_deletar_produto):
    assert not Produto.objects.exists()
