import pytest
from django.urls import reverse
from webdev.produtos.models import Produto, Categoria

# Novo Produto
@pytest.fixture
def resposta_novo_produto(client, db):
    categoria = Categoria.objects.create(nome='Brinco')
    resp = client.post(reverse('produtos:novo_produto'), data={
        'nome': 'Produto Legal',
        'colecao': "d'Mentira",
        'familia': 'Zanetti',
        'data_criacao': '2021-04-30',
        'unidades': 0,
        'tamanho': 22
    })
    return resp

def test_categoria_existe_no_bd(resposta_novo_produto):
    assert Categoria.objects.exists()

def test_produto_existe_no_bd(resposta_novo_produto):
    assert Produto.objects.exists()

def test_foto_padrao_do_produto(resposta_novo_produto):
    assert Produto.objects.first().foto.name == 'produtos/default.jpg'

