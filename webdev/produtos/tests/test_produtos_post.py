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

def test_redirecionamento_apos_salvamento(resposta):
    assert resposta.status_code == 302

@pytest.fixture
def resposta_invalida(client, db):
    resp = client.post(reverse('produtos:novo_produto'), data={})
    return resp

def test_novo_produto_nao_existe_no_bd(resposta_invalida):
    assert not Produto.objects.exists()

def test_pagina_com_dados_invalidos(resposta_invalida):
    assert resposta_invalida.status_code == 400

