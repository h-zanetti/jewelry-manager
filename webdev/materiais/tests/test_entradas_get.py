import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from webdev.materiais.models import Entrada, Material
from webdev.fornecedores.models import Fornecedor
from pytest_django.asserts import assertContains

# Lista de entradas
@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def lista_de_entradas(db, fornecedor):
    return [
        Entrada.objects.create(fornecedor=fornecedor, unidades=3, total_pago=1000),
        Entrada.objects.create(fornecedor=fornecedor, unidades=3, total_pago=3000)
    ]

@pytest.fixture
def lista_de_materiais(db, lista_de_entradas):
    materiais = []
    for entrada in lista_de_entradas:
        material = Material.objects.create(
            entrada=entrada,
            nome='Diamante',
            categoria='Pedra',
            qualidade=9,
            unidades=3
        )
        materiais.append(material)
    return materiais

@pytest.fixture
def resposta_entradas(client, lista_de_materiais):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:entradas'))
    return resp

def test_entradas_status_code(resposta_entradas):
    assert resposta_entradas.status_code == 200

def test_entradas_presente(resposta_entradas, lista_de_entradas):
    for entrada in lista_de_entradas:
        assertContains(resposta_entradas, entrada.fornecedor.nome)

def test_btn_entradas_presente(resposta_entradas):
    assertContains(resposta_entradas, f'<a href="{reverse("materiais:entradas")}"')

def test_btn_nova_entrada_presente(resposta_entradas):
    assertContains(resposta_entradas, f'<a href="{reverse("materiais:nova_entrada")}"')

def test_btn_editar_entrada_presente(resposta_entradas, lista_de_entradas, lista_de_materiais):
    for entrada in lista_de_entradas:
        assertContains(resposta_entradas, f'<a href="{reverse("materiais:editar_entrada", kwargs={"entrada_id": entrada.id, "material_id": entrada.get_material().id})}')

def test_btn_deletar_entrada_presente(resposta_entradas, lista_de_entradas):
    for entrada in lista_de_entradas:
        assertContains(resposta_entradas, f'<form action="{reverse("materiais:deletar_entrada", kwargs={"entrada_id": entrada.id})}')

def test_get_entradas_nao_autenticado_status_code(client, db):
    resp = client.get(reverse('materiais:entradas'))
    assert resp.status_code == 302

# Nova Entrada
@pytest.fixture
def resposta_nova_entrada(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:nova_entrada'))
    return resp

def test_nova_entrada_status_code(resposta_nova_entrada):
    assert resposta_nova_entrada.status_code == 200

def test_formulario_nova_entrada_presente(resposta_nova_entrada):
    assertContains(resposta_nova_entrada, f'<form action="{reverse("materiais:nova_entrada")}"')

def test_btn_submit_presente(resposta_nova_entrada):
    assertContains(resposta_nova_entrada, '<button type="submit"')
