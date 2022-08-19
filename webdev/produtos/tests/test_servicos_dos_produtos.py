import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.produtos.models import Produto, ServicoDoProduto

@pytest.fixture
def user(db):
    return User.objects.create_user(username='TestUser', password='MinhaSenha123')

@pytest.fixture
def produto1(db):
    p = Produto.objects.create(nome='Produto1', colecao="d'Mentira")
    ServicoDoProduto.objects.create(nome='Fotografia', produto=p, valor=2500)
    return p

# Visualização dos serviços no estoque de produtos
@pytest.fixture
def resposta_estoque_produtos(client, user, produto1):
    client.force_login(user)
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_servicos_do_produto_presente(resposta_estoque_produtos, produto1):
    for s in produto1.get_servicos():
        assertContains(resposta_estoque_produtos, s.nome)

def test_btn_adicionar_servico_presente(resposta_estoque_produtos, produto1):
    assertContains(
        resposta_estoque_produtos,
        f'<a href="{reverse("produtos:adicionar_servico", kwargs={"produto_id": produto1.id})}"'
    )

def test_btn_editar_servico_presente(resposta_estoque_produtos, produto1):
    for s in produto1.get_servicos():
        assertContains(
            resposta_estoque_produtos,
            f'<a href="{reverse("produtos:editar_servico_dp", kwargs={"servico_dp_id": s.id})}"'
        )

def test_btn_deletar_servico_presente(resposta_estoque_produtos, produto1):
    for s in produto1.get_servicos():
        assertContains(
            resposta_estoque_produtos,
            f'<form action="{reverse("produtos:remover_servico_dp", kwargs={"servico_dp_id": s.id})}"'
        )

# Adicionar serviço ao produto 
@pytest.fixture
def produto2(db):
    return Produto.objects.create(nome='Produto1', colecao="d'Mentira")

# GET
@pytest.fixture
def resposta_adicionar_servico_ao_produto_get(client, user, produto2):
    client.force_login(user)
    resp = client.get(reverse('produtos:adicionar_servico', kwargs={"produto_id": produto2.id}))
    return resp

def test_adicionar_servico_status_code(resposta_adicionar_servico_ao_produto_get):
    assert resposta_adicionar_servico_ao_produto_get.status_code == 200

def test_btn_submit_and_leave_present(resposta_adicionar_servico_ao_produto_get):
    assertContains(resposta_adicionar_servico_ao_produto_get, '<button type="submit" name="submit-leave"')

def test_btn_submit_and_stay_present(resposta_adicionar_servico_ao_produto_get):
    assertContains(resposta_adicionar_servico_ao_produto_get, '<button type="submit" name="submit-stay"')

# POST
@pytest.fixture
def resposta_adicionar_servico_dp(client, user, produto2):
    client.force_login(user)
    resp = client.post(
        reverse('produtos:adicionar_servico', kwargs={"produto_id": produto2.id}),
        data={
            'nome': 'Fotografia',
            'produto': produto2.id,
            'valor': 100.5,
        }
    )
    return resp

def test_adicionar_servico_redirect(resposta_adicionar_servico_dp):
    assertRedirects(resposta_adicionar_servico_dp,
        reverse('produtos:product_view', kwargs={'pk': 1}))

def test_servico_adicionado_ao_produto(resposta_adicionar_servico_dp):
    assert ServicoDoProduto.objects.exists()

def test_valor_do_produto_alterado(resposta_adicionar_servico_dp, produto2):
    assert produto2.get_custo_de_producao() == 100.5

# Editar servico do produto
@pytest.fixture
def servico_dp(produto2):
    return ServicoDoProduto.objects.create(nome='Fotografia', produto=produto2, valor=2000)

def test_get_editar_servico_dp(client, user, servico_dp):
    client.force_login(user)
    response = client.get(reverse('produtos:editar_servico_dp', kwargs={'servico_dp_id': servico_dp.id}))
    assert response.status_code == 200

@pytest.fixture
def resposta_editar_servico_dp(client, user, servico_dp):
    client.force_login(user)
    response = client.post(
        reverse('produtos:editar_servico_dp', kwargs={'servico_dp_id': servico_dp.id}),
        data={
            'nome': 'Fotografia',
            'valor': 1500
        }
    )
    return response

def test_editar_servico_dp_redirect(resposta_editar_servico_dp):
    assertRedirects(resposta_editar_servico_dp,
        reverse('produtos:product_view', kwargs={'pk': 1}))

def test_servico_dp_alterado(resposta_editar_servico_dp):
    assert ServicoDoProduto.objects.first().valor == 1500

def test_valor_do_produto_alterado2(resposta_editar_servico_dp, produto2):
    assert produto2.get_custo_de_producao() == 1500

# Remover servico do produto
@pytest.fixture
def resposta_remover_servico_dp(client, user, servico_dp):
    client.force_login(user)
    resp = client.post(reverse('produtos:remover_servico_dp', kwargs={'servico_dp_id': servico_dp.id}))
    return resp

def test_remover_servico_dp_status_code(resposta_remover_servico_dp):
    assertRedirects(resposta_remover_servico_dp,
        reverse('produtos:product_view', kwargs={'pk': 1}))

def test_servico_dp_deletado(resposta_remover_servico_dp):
    assert not ServicoDoProduto.objects.exists()
