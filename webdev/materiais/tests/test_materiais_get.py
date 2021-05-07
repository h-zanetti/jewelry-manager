import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from pytest_django.asserts import assertContains

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def entrada(fornecedor):
    return Entrada.objects.create(
        fornecedor=fornecedor,
        unidades=3,
        total_pago=1000
    )

@pytest.fixture
def material(entrada):
    return Material.objects.create(
        entrada=entrada,
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        unidades=3,
        peso=12,
        unidade_de_medida='g'
    )

# Estoque de matéria prima
@pytest.fixture
def resposta_estoque(client, material):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:estoque_materiais'))
    return resp

def test_estoque_materiais_status_code(resposta_estoque):
    assert resposta_estoque.status_code == 200

def test_materiais_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'{material.nome}')

def test_preco_unitario_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'R$ {material.get_preco_unitario()}'.replace('.', ','))

def test_preco_por_peso_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'R$ {material.get_preco_por_peso()}'.replace('.', ','))

def test_btn_estoque_materiais_presente(resposta_estoque):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:estoque_materiais")}"')

def test_btn_nova_entrada_presente(resposta_estoque):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:nova_entrada")}"')

def test_btn_editar_material_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'<a href="{reverse("materiais:editar_material", kwargs={"material_id": material.id})}"')

def test_btn_deletar_material_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f'<form action="{reverse("materiais:deletar_material", kwargs={"material_id": material.id})}"')

def test_get_entradas_nao_autenticado_status_code(client, db):
    resp = client.get(reverse('materiais:estoque_materiais'))
    assert resp.status_code == 302
