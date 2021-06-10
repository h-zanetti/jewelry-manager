import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.vendas.models import Cliente

# Visualizar Clientes
@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        nome="Henrique",
        sobrenome="Navaz",
        email="henrique.navaz@gmail.com",
        telefone="11966647420",
        endereco="Av. Localiza Aí Bebê, 240, Campo Belo, São Paulo, SP, 04613-030"
    )

@pytest.fixture
def resposta_clientes(client, cliente):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:clientes'))
    return resp

def test_despesas_status_code(resposta_clientes):
    assert resposta_clientes.status_code == 200

def test_lista_de_clientes_presente(resposta_clientes, cliente):
    assertContains(resposta_clientes, cliente)

def test_btn_novo_cliente_presente(resposta_clientes):
    assertContains(resposta_clientes, f'<a href="{reverse("vendas:novo_cliente")}')

def test_btn_editar_cliente_presente(resposta_clientes, cliente):
    assertContains(resposta_clientes, f'<a href="{reverse("vendas:editar_cliente", kwargs={"cliente_id": cliente.id})}')

def test_btn_deletar_cliente_presente(resposta_clientes, cliente):
    assertContains(resposta_clientes, f'<form action="{reverse("vendas:deletar_cliente", kwargs={"cliente_id": cliente.id})}')


# Novo Cliente
@pytest.fixture
def resposta_novo_cliente(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:novo_cliente'))
    return resp

def test_despesas_status_code(resposta_novo_cliente):
    assert resposta_novo_cliente.status_code == 200

def test_form_presente(resposta_novo_cliente):
    assertContains(resposta_novo_cliente, f'<form')

def test_btn_submit_stay_presente(resposta_novo_cliente):
    assertContains(resposta_novo_cliente, f'<button type="submit" name="submit-stay"')

def test_btn_submit_leave_presente(resposta_novo_cliente):
    assertContains(resposta_novo_cliente, f'<button type="submit" name="submit-leave"')


# Editar Cliente
@pytest.fixture
def resposta_editar_cliente(client, cliente):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('vendas:editar_cliente', kwargs={'cliente_id': cliente.id}))
    return resp

def test_editar_cliente_status_code(resposta_editar_cliente):
    assert resposta_editar_cliente.status_code == 200

def test_form_editar_cliente_presente(resposta_editar_cliente):
    assertContains(resposta_editar_cliente, f'<form')

def test_btn_submit_editar_cliente_presente(resposta_editar_cliente):
    assertContains(resposta_editar_cliente, f'<button type="submit"')
