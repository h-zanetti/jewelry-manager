import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from webdev.produtos.models import Produto
from django.contrib.auth.models import User

# Estoque
@pytest.fixture
def resposta_estoque_nao_autenticado(client, db):
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_estoque_produtos_nao_autenticado_status_code(resposta_estoque_nao_autenticado):
    resposta_estoque_nao_autenticado.status_code == 302

@pytest.fixture
def resposta_estoque_autenticado(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_estoque_produtos_autenticado_status_code(resposta_estoque_autenticado):
    assert resposta_estoque_autenticado.status_code == 200

def test_btn_novo_produto_presente(resposta_estoque_autenticado):
    assertContains(resposta_estoque_autenticado, f'''href="{reverse('produtos:novo_produto')}"''')

def test_btn_importar_produto_presente(resposta_estoque_autenticado):
    assertContains(resposta_estoque_autenticado, f'''href="{reverse('produtos:importar_produtos')}"''')

def test_btn_exportar_produto_presente(resposta_estoque_autenticado):
    assertContains(resposta_estoque_autenticado, f'''href="{reverse('produtos:exportar_produtos')}"''')

@pytest.fixture
def estoque_de_produtos(db):
    return [
        Produto.objects.create(nome='Produto1', colecao="d'Mentira", observacao="Essa é uma observação do produto."),
        Produto.objects.create(nome='Produto2', colecao="d'Mentira", observacao="Essa é uma observação do produto.")
    ]

@pytest.fixture
def resposta_com_estoque(client, estoque_de_produtos):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_estoque_de_produtos_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(resposta_com_estoque, produto.nome)

def test_preco_de_producao_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(resposta_com_estoque, f'R$ {produto.get_custo_de_producao()}'.replace('.', ','))

def test_btn_visualizar_produto_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(
            resposta_com_estoque,
            f'''<a href="#ModelProduto{produto.id}"'''
        )

def test_btn_editar_produto_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(
            resposta_com_estoque,
            f'''<a href="{reverse('produtos:editar_produto', kwargs={"produto_id": produto.id})}"'''
        )

def test_btn_deletar_produto_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(
            resposta_com_estoque,
            f'''<form action="{reverse('produtos:deletar_produto', kwargs={'produto_id': produto.id})}"'''
        )

def test_observacao_presente(resposta_com_estoque, estoque_de_produtos):
    for produto in estoque_de_produtos:
        assertContains(resposta_com_estoque, f"{produto.observacao}")

# Novo Produto
@pytest.fixture
def resposta_novo_produto(client, db):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:novo_produto'))
    return resp

def test_novo_produto_status_code(resposta_novo_produto):
    assert resposta_novo_produto.status_code == 200

def test_form_present(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<form')

def test_btn_submit_and_leave_present(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<button type="submit" name="submit-leave"')

def test_btn_submit_and_stay_present(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<button type="submit" name="submit-stay"')

def test_campo_observacao_presente(resposta_novo_produto):
    assertContains(resposta_novo_produto, '<textarea name="observacao"')


# Visualizar produto
@pytest.fixture
def product_view_response(client, estoque_de_produtos):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.force_login(usr)
    resp = client.get(reverse('produtos:product_view', kwargs={'pk': estoque_de_produtos[0].pk}))
    return resp

def test_product_view_status_code(product_view_response):
    assert product_view_response.status_code == 200

def test_product_name_present(product_view_response):
    produto = Produto.objects.first()
    assertContains(product_view_response, produto.nome)
