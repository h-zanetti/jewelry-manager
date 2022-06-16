import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.produtos.models import Produto, MaterialDoProduto

@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        estoque=3,
    )

@pytest.fixture
def entrada(material):
    return Entrada.objects.create(
        material=material,
        data='2021-04-26',
        peso=5,
        unidade_de_medida='g',
        valor=2500,
        alterar_estoque=True,
    )

@pytest.fixture
def produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

# Adicionar Material ao Produto
@pytest.fixture
def resposta_adicionar_material_do_produto(client, produto, material, user, entrada):
    client.force_login(user)
    resp = client.post(
        reverse('produtos:adicionar_material', kwargs={'produto_id': produto.id}),
        data={
            'produto': produto.id,
            'material': material.id,
            'unidades': 1,
            'peso': 2.5,
            'unidade_de_medida': 'g',
        }
    )
    return resp

# For debug purposes only
# def test_form_is_valid(resposta_adicionar_material_do_produto):
#     assert not resposta_adicionar_material_do_produto.context['form'].errors

def test_adicionar_material_do_produto_status_code(resposta_adicionar_material_do_produto):
    assertRedirects(
        resposta_adicionar_material_do_produto,
        reverse('produtos:estoque_produtos')
    )

def test_material_adicionado_ao_produto(resposta_adicionar_material_do_produto):
    assert MaterialDoProduto.objects.exists()

def test_custo_do_produto_alterado(resposta_adicionar_material_do_produto):
    assert Produto.objects.first().get_custo_de_producao() == 1250

# Editar Material ao Produto
@pytest.fixture
def material_do_produto(produto, material):
    return MaterialDoProduto.objects.create(
        produto=produto,
        material=material,
        unidades=1,
        peso=2.5,
        unidade_de_medida='g',
    )

@pytest.fixture
def resposta_editar_material_do_produto(client, material_do_produto, user, produto, material, entrada):
    client.force_login(user)
    resp = client.post(
        reverse('produtos:editar_material_dp', kwargs={'material_dp_id': material_do_produto.id}),
        data={
            'produto': produto.id,
            'material': material.id,
            'unidades': 1,
            'peso': 1.5,
            'unidade_de_medida': 'g',
        }
    )
    return resp

def test_editar_material_do_produto_status_code(resposta_editar_material_do_produto):
    assert resposta_editar_material_do_produto.status_code == 302

def test_material_do_produto_editado(resposta_editar_material_do_produto):
    assert MaterialDoProduto.objects.first().peso == 1.5

def test_custo_do_produto_alterado2(resposta_editar_material_do_produto):
    assert Produto.objects.first().get_custo_de_producao() == 750


# Remover Material ao Produto
@pytest.fixture
def resposta_remover_material_do_produto(client, material_do_produto, user):
    client.force_login(user)
    resp = client.post(reverse(
        'produtos:remover_material_dp',
        kwargs={'material_dp_id': material_do_produto.id}))
    return resp

def test_remover_material_do_produto_status_code(resposta_remover_material_do_produto):
    assert resposta_remover_material_do_produto.status_code == 302

def test_material_do_produto_deletado(resposta_remover_material_do_produto):
    assert not MaterialDoProduto.objects.exists()
