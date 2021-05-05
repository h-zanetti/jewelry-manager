import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.produtos.models import Produto
from webdev.fornecedores.models import Fornecedor, Servico

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def servico(fornecedor):
    return Servico.objects.create(
        nome='Fotografia',
        data='2021-04-05',
        fornecedor=fornecedor,
        qualidade=5,
        total_pago=100.5
    )

@pytest.fixture
def produto_com_servico(servico):
    p = Produto.objects.create(nome='Produto1', colecao="d'Mentira")
    p.servicos.add(servico)
    return p

# Visualização dos serviços no estoque de produtos
@pytest.fixture
def resposta_estoque_produtos(client, produto_com_servico, fornecedor, servico):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:estoque_produtos'))
    return resp

def test_servicos_do_produto_presente(resposta_estoque_produtos, produto_com_servico):
    for s in produto_com_servico.servicos.all():
        assertContains(resposta_estoque_produtos, s.nome)

def test_btn_adicionar_servico_presente(resposta_estoque_produtos, produto_com_servico):
    assertContains(
        resposta_estoque_produtos,
        f'<a href="{reverse("produtos:adicionar_servico", kwargs={"produto_id": produto_com_servico.id})}"'
    )

def test_btn_editar_servico_presente(resposta_estoque_produtos, produto_com_servico):
    for s in produto_com_servico.servicos.all():
        assertContains(
            resposta_estoque_produtos,
            f'<a href="{reverse("fornecedores:editar_servico", kwargs={"servico_id": s.id})}"'
        )

def test_btn_deletar_servico_presente(resposta_estoque_produtos, produto_com_servico):
    for s in produto_com_servico.servicos.all():
        assertContains(
            resposta_estoque_produtos,
            f'<form action="{reverse("fornecedores:deletar_servico", kwargs={"servico_id": s.id})}"'
        )

# Adicionar serviço ao produto
@pytest.fixture
def produto_sem_servico(db):
    return Produto.objects.create(nome='Produto1', colecao="d'Mentira")

@pytest.fixture
def resposta_adicionar_servico_ao_produto(client, produto_sem_servico, fornecedor):
    usr = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:adicionar_servico', kwargs={"produto_id": produto_sem_servico.id}),
        data={
            'nome': 'Fotografia',
            'data': '04-05-2021',
            'fornecedor': fornecedor.id,
            'qualidade': 5,
            'total_pago': 100.5
        }
    )
    return resp

def test_adicionar_servico_ao_produto_status_code(resposta_adicionar_servico_ao_produto, produto_sem_servico):
    assert resposta_adicionar_servico_ao_produto.status_code == 302

def test_servico_adicionado_ao_produto(resposta_adicionar_servico_ao_produto, produto_sem_servico):
    assert produto_sem_servico.servicos.exists()
