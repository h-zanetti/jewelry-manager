import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.produtos.models import Categoria

@pytest.fixture
def categorias(db):
    return [
        Categoria.objects.create(nome='Anel'),
        Categoria.objects.create(nome='Brinco'),
        Categoria.objects.create(nome='Colar'),
    ]

# GET
@pytest.fixture
def resposta_categorias(client, categorias):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('produtos:categorias'))
    return resp

def test_categorias_existentes_presente(resposta_categorias, categorias):
    for categoria in categorias:
        assertContains(resposta_categorias, categoria.nome)

def test_form_nova_categoria_presente(resposta_categorias, categorias):
    assertContains(resposta_categorias, f'<input type="text" name="form-{len(categorias)}-nome"')

# POST
@pytest.fixture
def resposta_categorias_post(client, categorias):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('produtos:categorias'),
        data={
            'form-TOTAL_FORMS': len(categorias)+1, # Um formulário para cada categoria existente e mais um para uma nova categoria
            'form-INITIAL_FORMS': len(categorias),
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-0-id': 1,
            'form-0-nome': 'Pingente', # Alterar nome da categoria de id=1
            'form-0-DELETE': False,
            'form-1-id': 2,
            'form-1-nome': 'Brinco',
            'form-1-DELETE': False,
            'form-2-id': 3,
            'form-2-nome': 'Colar',
            'form-2-DELETE': True, # Deletar categoria de id=3
            'form-3-nome': 'Aliança', # Criar nova categoria
            'form-3-DELETE': False,
        }
    )
    return resp

def test_resposta_status_code(resposta_categorias_post, categorias):
    assert resposta_categorias_post.status_code == 302

def test_primeira_categoria_alterada(resposta_categorias_post):
    assert Categoria.objects.first().nome == 'Pingente'

def test_categoria_colar_deletada(resposta_categorias_post):
    assert not Categoria.objects.filter(nome='Colar')

def test_nova_categoria_criada(resposta_categorias_post):
    assert Categoria.objects.last().nome == 'Aliança'

