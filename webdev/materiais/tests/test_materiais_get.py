import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Material
from pytest_django.asserts import assertContains

@pytest.fixture
def material(db):
    return Material.objects.create(
        unidades_compradas=3,
        total_pago=1000,
        nome='Esmeralda',
        categoria='Pedra',
        qualidade=5,
        estoque=3,
        observacao="Incididunt cupidatat occaecat laborum minim nisi esse proident nostrud aliqua sint sit ad."
    )

# Estoque de matéria prima
@pytest.fixture
def resposta_estoque(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
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

def test_observacao_presente(resposta_estoque, material):
    assertContains(resposta_estoque, f"{material.observacao}")


# Nova Entrada de Matéria Prima
@pytest.fixture
def resposta_nova_entrada(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:nova_entrada'))
    return resp

def test_nova_entrada_status_code(resposta_nova_entrada):
    assert resposta_nova_entrada.status_code == 200

def test_btn_submit_stay_presente(resposta_nova_entrada):
    assertContains(resposta_nova_entrada, '<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_nova_entrada):
    assertContains(resposta_nova_entrada, '<button type="submit" name="submit-leave"')

def test_campo_observacao_presente(resposta_nova_entrada):
    assertContains(resposta_nova_entrada, '<textarea name="observacao"')