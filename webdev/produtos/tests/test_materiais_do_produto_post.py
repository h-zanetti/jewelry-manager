import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor
from webdev.materiais.models import Entrada, Material
from webdev.produtos.models import Produto, MaterialDoProduto

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def entrada(fornecedor):
    return Entrada.objects.create(fornecedor=fornecedor, unidades=3, total_pago=1000)

@pytest.fixture
def material(entrada):
    return Material.objects.create(
        entrada=entrada,
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        unidades=3
    )

@pytest.fixture
def produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

# Adicionar Material ao Produto
@pytest.fixture
def resposta_adicionar_material_do_produto(client, produto, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:adicionar_material', kwargs={'produto_id': produto.id}),
        data={
            'material': material.id,
            'unidades': 1,
        }
    )
    return resp

def test_adicionar_material_do_produto_status_code(resposta_adicionar_material_do_produto):
    assert resposta_adicionar_material_do_produto.status_code == 302

def test_material_adicionado_ao_produto(resposta_adicionar_material_do_produto):
    assert MaterialDoProduto.objects.exists()


# Editar Material ao Produto
@pytest.fixture
def material_do_produto(produto, material):
    material_dp = MaterialDoProduto.objects.create(
        material=material,
        unidades=1
    )
    produto.materiais.add(material_dp)
    return material_dp

@pytest.fixture
def resposta_editar_material_do_produto(client, material_do_produto):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:editar_material_dp', kwargs={'material_dp_id': material_do_produto.id}),
        data={
            'material': material.id,
            'unidades': 2,
        }
    )
    return resp

def test_editar_material_do_produto_status_code(resposta_editar_material_do_produto):
    assert resposta_editar_material_do_produto.status_code == 302

def test_material_do_produto_editado(resposta_editar_material_do_produto):
    assert MaterialDoProduto.objects.first().unidades == 2


# Remover Material ao Produto
@pytest.fixture
def resposta_remover_material_do_produto(client, material_do_produto):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('produtos:remover_material_dp', kwargs={'material_dp_id': material_do_produto.id}))
    return resp

def test_editar_material_do_produto_status_code(resposta_remover_material_do_produto):
    assert resposta_remover_material_do_produto.status_code == 302

def test_material_do_produto_editado(resposta_remover_material_do_produto):
    assert not MaterialDoProduto.objects.exists()