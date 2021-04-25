import pytest
from django.urls import reverse

@pytest.fixture
def resposta(client):
    resp = client.get(reverse('produtos:estoque'))
    return resp

def test_produtos_estoque_status_code(resposta):
    assert resposta.status_code == 200