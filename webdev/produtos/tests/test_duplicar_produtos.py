import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects
from webdev.produtos.models import Produto, MaterialDoProduto
from webdev.materiais.models import Material
from webdev.fornecedores.models import Servico
from django.contrib.auth.models import User

@pytest.fixture
def produto(db):
    return Produto.objects.create(nome='Produto1', colecao="d'Mentira", tamanho=18)

# GET
@pytest.fixture
def resposta_get_duplicar_produto(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:duplicar_produto', kwargs={'produto_id': produto.id}))
    return resp

def test_resposta_status_code_get(resposta_get_duplicar_produto):
    assert resposta_get_duplicar_produto.status_code == 200

def test_dados_do_produto_presente(resposta_get_duplicar_produto, produto):
    assertContains(resposta_get_duplicar_produto, produto.nome)

# POST
@pytest.fixture
def resposta_post_duplicar_produto(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:duplicar_produto', kwargs={'produto_id': produto.id}),
        data = {
            'nome': 'Produto1',
            'colecao': "d'Mentira",
            'tamanho': 25,
            'unidades': 1,
        }
    )
    return resp

def test_resposta_status_code_post(resposta_post_duplicar_produto):
    assert resposta_post_duplicar_produto.status_code == 302

def test_produto_original_inalterado(resposta_post_duplicar_produto):
    assert Produto.objects.first().tamanho == 18

def test_produto_duplicado_existe(resposta_post_duplicar_produto):
    assert len(Produto.objects.all()) > 1

def test_produto_duplicado_tamanho_diferente(resposta_post_duplicar_produto):
    assert Produto.objects.last().tamanho == 25

# Visualização
@pytest.fixture
def resposta_estoque(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_btn_clonar_produto_presente(resposta_estoque, produto):
    assertContains(resposta_estoque, f'href="{reverse("produtos:duplicar_produto", kwargs={"produto_id": produto.id})}"')

# Redirecionamento
# Submit and stay
@pytest.fixture
def resposta_duplicar_produto_e_continuar(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:duplicar_produto', kwargs={'produto_id': produto.id}),
        data = {
            'nome': 'Produto1',
            'colecao': "d'Mentira",
            'tamanho': 25,
            'unidades': 1,
            'submit-stay': True
        }
    )
    return resp

def test_submit_and_stay(resposta_duplicar_produto_e_continuar):
    produto = Produto.objects.last()
    assertRedirects(
        resposta_duplicar_produto_e_continuar,
        reverse('produtos:duplicar_produto', kwargs={'produto_id': produto.id})
    )

# Submit and leave
@pytest.fixture
def resposta_duplicar_produto_e_voltar(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:duplicar_produto', kwargs={'produto_id': produto.id}),
        data = {
            'nome': 'Produto1',
            'colecao': "d'Mentira",
            'tamanho': 25,
            'unidades': 1,
            'submit-leave': True
        }
    )
    return resp

def test_submit_and_stay(resposta_duplicar_produto_e_voltar):
    produto = Produto.objects.last()
    assertRedirects(
        resposta_duplicar_produto_e_voltar, reverse('produtos:estoque_produtos')
    )
