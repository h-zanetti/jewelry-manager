import pytest
from django.urls import reverse
from django.utils import timezone
from webdev.financeiro.models import Despesa
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User, Permission

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='TestUser', password='MinhaSenha123')
    permissions = Permission.objects.filter(content_type__app_label='financeiro', content_type__model='despesa')
    user.user_permissions.set(permissions)
    return user

# Nova Despesa
@pytest.fixture
def resposta_nova_despesa(client, user):
    client.force_login(user)
    resp = client.post(
        reverse('financeiro:nova_despesa'),
        data={
            'data': '26-04-2021',
            'categoria': 'MEI',
            'valor': 75,
            'repetir': 'm'
        }
    )
    return resp

def test_despesas_status_code(resposta_nova_despesa):
    assert resposta_nova_despesa.status_code == 302

def test_nova_despesa_criada(resposta_nova_despesa):
    assert Despesa.objects.exists()

# Editar Despesas
@pytest.fixture
def despesa(db):
    return Despesa.objects.create(
        data=timezone.localdate(),
        categoria='MEI',
        valor=75,
        repetir='m'
    )

@pytest.fixture
def resposta_editar_despesa(client, despesa, user):
    client.force_login(user)
    resp = client.post(
        reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesa.id}),
        data={
            'data': timezone.localdate().strftime('%d-%m-%Y'),
            'categoria': 'Manutenção',
            'valor': 75,
            'repetir': 'm',
        }
    )
    return resp

def test_editar_despesa_status_code(resposta_editar_despesa):
    assert resposta_editar_despesa.status_code == 302

def test_despesa_editada(resposta_editar_despesa):
    assert Despesa.objects.first().categoria == 'Manutenção'

# Encerrar Despesa
@pytest.fixture
def resposta_encerrar_despesa(client, despesa, user):
    client.force_login(user)
    st_date = timezone.localdate() - relativedelta(years=1, months=3)
    resp = client.post(
        reverse('financeiro:editar_despesa', kwargs={'despesa_id': despesa.id}),
        data={
            'data': st_date.strftime('%d-%m-%Y'),
            'categoria': 'MEI',
            'valor': 75,
            'repetir': 'm',
            'data_de_encerramento': timezone.localdate().strftime('%d-%m-%Y'),
        }
    )
    return resp

def test_editar_despesa_status_code(resposta_encerrar_despesa):
    assert resposta_encerrar_despesa.status_code == 302

def test_data_de_encerramento_alterada(resposta_encerrar_despesa):
    assert Despesa.objects.first().data_de_encerramento == timezone.localdate()

# Deletar Despesa
@pytest.fixture
def resposta_deletar_despesa(client, despesa, user):
    client.force_login(user)
    resp = client.post(reverse('financeiro:deletar_despesa', kwargs={'despesa_id': despesa.id}))
    return resp

def test_deletar_despesa_status_code(resposta_deletar_despesa):
    assert resposta_deletar_despesa.status_code == 302

def test_despesa_deletada(resposta_deletar_despesa):
    assert not Despesa.objects.exists()

