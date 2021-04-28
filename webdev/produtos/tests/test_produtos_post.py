import pytest
from django.urls import reverse
from webdev.produtos.models import Produto

@pytest.fixture
def resposta(client, db):
    resp = client.post(reverse('produtos:novo_produto'), data={
        'nome': 'Produto Legal',
        'colecao': "d'Mentira",
        'data_criacao': '2021-04-26',
        'quantidade': 5,
        'tamanho': 22
    })
    return resp

def test_novo_produto_existe_no_bd(resposta):
    assert Produto.objects.exists()