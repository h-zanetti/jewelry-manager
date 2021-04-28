import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

@pytest.fixture
def resposta(client, db):
    resp = client.get(reverse('produtos:novo_produto'))
    return resp

def test_novo_produto_status_code(resposta):
    assert resposta.status_code == 200

def test_novo_produto_form_presente(resposta):
    assertContains(resposta, '<form')

def test_novo_produto_btn_de_submit_presente(resposta):
    assertContains(resposta, '<button type="submit"')

