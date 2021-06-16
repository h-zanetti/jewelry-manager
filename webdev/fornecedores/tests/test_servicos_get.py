import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecedor, Servico

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

# Novo Serviço
@pytest.fixture
def resposta_novo_servico(client, fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:novo_servico'))
    return resp

def test_novo_servico_status_code(resposta_novo_servico):
    assert resposta_novo_servico.status_code == 200

def test_btn_submit_stay_presente(resposta_novo_servico):
    assertContains(resposta_novo_servico, '<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_novo_servico):
    assertContains(resposta_novo_servico, '<button type="submit" name="submit-leave"')

# Visualização de serviços
@pytest.fixture
def servico(fornecedor):
    return Servico.objects.create(
        nome='Fotografia',
        data='2021-04-05',
        fornecedor=fornecedor,
        qualidade=5,
        valor=100.5
    )

@pytest.fixture
def resposta_meus_fornecedores_com_servico(client, fornecedor, servico):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:meus_fornecedores'))
    return resp

def test_servicos_presente(resposta_meus_fornecedores_com_servico, servico):
    assertContains(resposta_meus_fornecedores_com_servico, servico.nome)

def test_btn_editar_servicos_presente(resposta_meus_fornecedores_com_servico, servico):
    assertContains(
        resposta_meus_fornecedores_com_servico,
        f'<a href="{reverse("fornecedores:editar_servico", kwargs={"servico_id": servico.id})}"'
    )

def test_btn_deletar_servicos_presente(resposta_meus_fornecedores_com_servico, servico):
    assertContains(
        resposta_meus_fornecedores_com_servico,
        f'<form action="{reverse("fornecedores:deletar_servico", kwargs={"servico_id": servico.id})}"'
    )

#  Edição de Serviços
@pytest.fixture
def resposta_editar_servico(client, fornecedor, servico):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:editar_servico', kwargs={'servico_id': servico.id}))
    return resp

def test_get_editar_servico(resposta_editar_servico):
    assert resposta_editar_servico.status_code == 200
