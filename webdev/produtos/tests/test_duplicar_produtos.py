import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects
from webdev.produtos.models import Produto, MaterialDoProduto, ServicoDoProduto
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Servico
from django.contrib.auth.models import User

@pytest.fixture
def produto(db):
    return Produto.objects.create(nome='Produto1', colecao="d'Mentira", tamanho=18)

# Visualização
@pytest.fixture
def resposta_estoque(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_btn_clonar_produto_presente(resposta_estoque, produto):
    assertContains(resposta_estoque, f'href="{reverse("produtos:duplicar_produto", kwargs={"produto_id": produto.id})}"')

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

# Fixtures
@pytest.fixture
def material(db):
    return Material.objects.create(
    nome='Esmeralda',
    categoria='Pedra',
)

@pytest.fixture
def entrada(material):
    return Entrada.objects.create(
        material=material,
        data='2021-04-26',
        unidades=3,
        valor=1000
    )

@pytest.fixture
def material_dp(produto, material):
    return MaterialDoProduto.objects.create(
        produto=produto,
        material=material,
        unidades=1,
    )

@pytest.fixture
def servico_dp(produto):
    return ServicoDoProduto.objects.create(
        produto=produto,
        nome='Fotografia',
        valor=3000,
    )

# POST
@pytest.fixture
def resposta_post_duplicar_produto(client, produto, material, entrada, material_dp, servico_dp):
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

def test_redirecionamento_duplicar_produto(resposta_post_duplicar_produto):
    assertRedirects(
        resposta_post_duplicar_produto,
        reverse('produtos:estoque_produtos')
    )

def test_produto_original_inalterado(resposta_post_duplicar_produto):
    assert Produto.objects.first().tamanho == 18

def test_produto_duplicado(resposta_post_duplicar_produto):
    assert len(Produto.objects.all()) > 1

def test_tamanho_alterado(resposta_post_duplicar_produto):
    assert Produto.objects.last().tamanho == 25

def test_material_dp_duplicado(resposta_post_duplicar_produto):
    assert len(MaterialDoProduto.objects.all()) > 1

def test_servico_dp_duplicado(resposta_post_duplicar_produto):
    assert len(ServicoDoProduto.objects.all()) > 1

def test_custo_duplicado(resposta_post_duplicar_produto):
    assert float(Produto.objects.last().get_custo_de_producao()) == 3333.33
