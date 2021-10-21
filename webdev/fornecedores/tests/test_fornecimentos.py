import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from django.contrib.auth.models import User
from webdev.fornecedores.models import Fornecimento

@pytest.fixture
def fornecimentos(db):
    return [
        Fornecimento.objects.create(nome='Programador', qualidade=10),
        Fornecimento.objects.create(nome='Diretor de Arte', qualidade=6),
    ]

# GET
@pytest.fixture
def resposta_fornecimentos(client, fornecimentos):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(reverse('fornecedores:fornecimentos'))
    return resp

def test_resposta_status_code_get(resposta_fornecimentos, fornecimentos):
    assert resposta_fornecimentos.status_code == 200

def test_btn_fornecimentos_presente(resposta_fornecimentos):
    assertContains(resposta_fornecimentos, f'href="{reverse("fornecedores:fornecimentos")}"')

def test_fornecimentos_existentes_presente(resposta_fornecimentos, fornecimentos):
    for fornecimento in fornecimentos:
        assertContains(resposta_fornecimentos, fornecimento.nome)

def test_form_novo_fornecimento_presente(resposta_fornecimentos, fornecimentos):
    assertContains(resposta_fornecimentos, f'<input type="text" name="form-{len(fornecimentos)}-nome"')

def test_btn_submit_and_stay_presente(resposta_fornecimentos):
    assertContains(resposta_fornecimentos, '<button type="submit" name="submit-stay"')

def test_btn_submit_and_leave_presente(resposta_fornecimentos):
    assertContains(resposta_fornecimentos, '<button type="submit" name="submit-leave"')

# POST
@pytest.fixture
def resposta_fornecimentos_post(client, fornecimentos):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.post(
        reverse('fornecedores:fornecimentos'),
        data={
            'form-TOTAL_FORMS': len(fornecimentos)+1,
            'form-INITIAL_FORMS': len(fornecimentos),
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
            'form-0-id': 1,
            'form-0-nome': 'Programador',
            'form-0-qualidade': 9, # Alterar qualidade
            'form-0-DELETE': False,
            'form-1-id': 2,
            'form-1-nome': 'Diretor de Arte',
            'form-1-qualidade': 6,
            'form-1-DELETE': True, # Remover Diretor de Arte
            'form-2-nome': 'Designer', # Adicionar Designer
            'form-2-qualidade': 6,
        }
    )
    return resp

def test_resposta_status_code_post(resposta_fornecimentos_post):
    assert resposta_fornecimentos_post.status_code == 302

def test_primeiro_fornecimento_alterado(resposta_fornecimentos_post):
    assert Fornecimento.objects.first().qualidade == 9

def test_segundo_fornecimento_deletado(resposta_fornecimentos_post):
    assert not Fornecimento.objects.filter(nome='Diretor de Arte')

def test_terceiro_fornecimento_adicionado(resposta_fornecimentos_post):
    assert Fornecimento.objects.last().nome == 'Designer'

