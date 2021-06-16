import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from webdev.produtos.models import Produto, MaterialDoProduto

@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        unidades_compradas=3,
        estoque=3,
        valor=1000,
    )

@pytest.fixture
def produto(db):
    return Produto.objects.create(
        nome='Produto Legal',
        colecao="d'Mentira",
    )

@pytest.fixture
def material_do_produto(produto, material):
    material_dp = MaterialDoProduto.objects.create(
        material=material,
        unidades=1
    )
    produto.materiais.add(material_dp)
    return material_dp

# Visualização 
@pytest.fixture
def resposta_estoque(client, material_do_produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_material_do_produto_presente(resposta_estoque, material_do_produto):
    assertContains(resposta_estoque, f'<td>{material_do_produto.material.nome}')

def test_btn_adicionar_material_ao_produto_presente(resposta_estoque, produto):
    assertContains(resposta_estoque, f'<a href="{reverse("produtos:adicionar_material", kwargs={"produto_id": produto.id})}')

def test_btn_editar_material_do_produto_presente(resposta_estoque, material_do_produto):
    assertContains(
        resposta_estoque,
        f'<a href="{reverse("produtos:editar_material_dp", kwargs={"material_dp_id": material_do_produto.id})}'
    )

def test_btn_remover_material_do_produto_presente(resposta_estoque, material_do_produto):
    assertContains(
        resposta_estoque,
        f'<form action="{reverse("produtos:remover_material_dp", kwargs={"material_dp_id": material_do_produto.id})}'
    )

# Adicionar Material ao Produto
@pytest.fixture
def resposta_adicionar_material_do_produto(client, produto):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('produtos:adicionar_material', kwargs={'produto_id': produto.id})
    )
    return resp

def test_adicionar_material_do_produto_status_code(resposta_adicionar_material_do_produto):
    assert resposta_adicionar_material_do_produto.status_code == 200

def test_form_present(resposta_adicionar_material_do_produto):
    assertContains(resposta_adicionar_material_do_produto, '<form')

def test_btn_submit_and_leave_present(resposta_adicionar_material_do_produto):
    assertContains(resposta_adicionar_material_do_produto, '<button type="submit" name="submit-leave"')

def test_btn_submit_and_stay_present(resposta_adicionar_material_do_produto):
    assertContains(resposta_adicionar_material_do_produto, '<button type="submit" name="submit-stay"')

