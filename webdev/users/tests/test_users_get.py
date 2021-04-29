import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

# Login
@pytest.fixture
def resposta(client):
    resp = client.get(reverse('login'))
    return resp

def test_pagina_de_login_status_code(resposta):
    assert resposta.status_code == 200

def test_form_present(resposta):
    assertContains(resposta, '<form')

def test_link_redefinir_senha_presente(resposta):
    assertContains(resposta, f'''<a href="{reverse('password_reset')}"''')

def test_btn_submit_present(resposta):
    assertContains(resposta, '<button type="submit"')

# Password reset
def test_pagina_de_login_status_code(client):
    resposta = client.get(reverse('password_reset'))
    assert resposta.status_code == 200

# Password reset done
def test_pagina_de_login_status_code(client):
    resposta = client.get(reverse('password_reset_done'))
    assert resposta.status_code == 200

# Password reset complete
def test_pagina_de_login_status_code(client):
    resposta = client.get(reverse('password_reset_complete'))
    assert resposta.status_code == 200

