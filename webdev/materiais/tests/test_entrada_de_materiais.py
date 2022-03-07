from webdev.financeiro.models import Despesa
from webdev.materiais.models import Entrada, Material
import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User

# Entrada de materiais lista (GET)
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
        peso=0.17,
        unidade_de_medida='ct',
        valor=1000
    )

@pytest.fixture
def resposta_entradas(client, entrada):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:entradas_de_materiais'))
    return resp

def test_entradas_de_materiais_status_code(resposta_entradas):
    assert resposta_entradas.status_code == 200

def test_entrada_presente(resposta_entradas, entrada):
    assertContains(resposta_entradas, str(entrada))

def test_material_presente(resposta_entradas, material):
    assertContains(resposta_entradas, material.nome)

def test_btn_editar_entrada_presente(resposta_entradas, entrada):
    assertContains(resposta_entradas, f'<a href="{reverse("materiais:editar_entrada", kwargs={"entrada_id": entrada.id})}"')

def test_btn_deletar_entrada_presente(resposta_entradas, entrada):
    assertContains(resposta_entradas, f'<form action="{reverse("materiais:deletar_entrada", kwargs={"entrada_id": entrada.id})}"')

def test_btn_importar_entrada_presente(resposta_entradas, entrada):
    assertContains(resposta_entradas, f'<a href="{reverse("materiais:importar_entradas")}"')

def test_btn_exportar_entrada_presente(resposta_entradas, entrada):
    assertContains(resposta_entradas, f'<a href="{reverse("materiais:exportar_entradas")}"')


# Entrada de materiais form (GET)
@pytest.fixture
def resposta_form_de_entrada(client, db):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('materiais:entrada_de_material'))
    return resp

def test_cadastrar_material_status_code(resposta_form_de_entrada):
    assert resposta_form_de_entrada.status_code == 200

def test_form_presente(resposta_form_de_entrada):
    assertContains(
        resposta_form_de_entrada,
        f'<form action="{reverse("materiais:entrada_de_material")}"'
    )

def test_btn_submit_stay_presente(resposta_form_de_entrada):
    assertContains(resposta_form_de_entrada, '<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_form_de_entrada):
    assertContains(resposta_form_de_entrada, '<button type="submit" name="submit-leave"')

# Criar entrada de materiais (POST)
@pytest.fixture
def resposta_entrada_de_material(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:entrada_de_material'), data={
        'data': '2021-04-26',
        'material': material.id,
        'unidades': 5,
        'peso': 5,
        'unidade_de_medida': 'g',
        'valor': 3000,
        'alterar_estoque': True,
    })
    return resp

# def test_form_sem_erros(resposta_entrada_de_material):
#     assert not resposta_entrada_de_material.context['form'].errors

def test_entrada_de_material_redirect(resposta_entrada_de_material):
    assertRedirects(resposta_entrada_de_material, reverse('materiais:estoque_materiais'))

def teste_despesa_criada(resposta_entrada_de_material):
    assert Despesa.objects.exists()

def test_estoque_de_material_alterado_unidades(resposta_entrada_de_material, material):
    m = Material.objects.get(pk=material.pk)
    assert m.estoque == 5

def test_estoque_de_material_alterado_peso(resposta_entrada_de_material, material):
    m = Material.objects.get(pk=material.pk)
    assert m.peso == 5

# Testar validação de unidade de medida
@pytest.fixture
def material(db):
    return Material.objects.create(
        nome='Esmeralda',
        categoria='Pedra',
        peso=0,
        unidade_de_medida='g'
    )

@pytest.fixture
def resposta_entrada_de_material_invalid(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:entrada_de_material'), data={
        'data': '2021-04-26',
        'material': material.id,
        'unidades': 5,
        'peso': 5,
        'unidade_de_medida': 'ct',
        'valor': 3000
    })
    return resp

def test_invalid_form(resposta_entrada_de_material_invalid):
    assert resposta_entrada_de_material_invalid.status_code == 200

def test_unidade_de_medida_error(resposta_entrada_de_material_invalid):
    assert 'unidade_de_medida' in resposta_entrada_de_material_invalid.context['form'].errors


# Entrada de materiais sem alterar o estoque (POST)
@pytest.fixture
def resposta_entrada_sem_estoque(client, material):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(reverse('materiais:entrada_de_material'), data={
        'data': '2021-04-26',
        'material': material.id,
        'unidades': 5,
        'peso': 5,
        'unidade_de_medida': 'g',
        'valor': 3000,
        'alterar_estoque': False,
    })
    return resp

# def test_form_sem_erros(resposta_entrada_sem_estoque):
#     assert not resposta_entrada_sem_estoque.context['form'].errors

def test_redirect_entrada_sem_estoque(resposta_entrada_sem_estoque):
    assertRedirects(resposta_entrada_sem_estoque, reverse('materiais:estoque_materiais'))

def teste_despesa_sem_estoque_criada(resposta_entrada_sem_estoque):
    assert Despesa.objects.exists()

def test_estoque_de_material_sem_alterar_unidades(resposta_entrada_sem_estoque):
    assert Material.objects.first().estoque == 0

def test_estoque_de_material_sem_alterar_peso(resposta_entrada_sem_estoque):
    assert Material.objects.first().peso == 0
