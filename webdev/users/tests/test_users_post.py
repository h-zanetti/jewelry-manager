import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from pytest_django.asserts import assertRedirects

@pytest.fixture
def resposta(client, db):
    usr = User.objects.create_user(username='UserTest', password='minhaSenha123')
    resp = client.post(reverse('login'), data={'username': 'UserTest', 'password': 'minhaSenha123'})
    return resp

def test_user_autenticado(resposta):
    assert resposta.wsgi_request.user.is_authenticated == True

def test_redirecionamento(resposta):
    assertRedirects(resposta, reverse('produtos:estoque_produtos'))