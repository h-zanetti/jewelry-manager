from calendar import monthrange
from django.db.models.query_utils import Q
from webdev.fornecedores.models import Fornecedor, Servico
from django.db.models.functions import TruncMonth
from dateutil.relativedelta import relativedelta
from django.db.models.aggregates import Sum
import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains, assertNotContains
from django.contrib.auth.models import User
from webdev.financeiro.models import Despesa, Parcela
from webdev.vendas.models import Cliente, Venda
from webdev.produtos.models import Produto
from webdev.materiais.models import Material

@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        nome="Henrique",
        sobrenome="Navaz",
        email="henrique.navaz@gmail.com",
        telefone="11966647420",
        endereco="Av. Localiza Aí Bebê, 240, Campo Belo, São Paulo, SP, 04613-030"
    )

@pytest.fixture
def lista_de_produtos(db):
    return [
        Produto.objects.create(nome='Anel', colecao="d'Mentira"),
        Produto.objects.create(nome='Brinco', colecao="d'Mentira"),
        Produto.objects.create(nome='Bracelete', colecao="d'Mentira")
    ]

'''
Objetos do tipo Parcela e Receita são criados, edidatos ou deletados automaticamente ao salvar, editar ou 
deletar um objeto do tipo Venda. Para mais informações, ver tests do arquivo test_vendas_post.py ou as 
funções em webdev.financeiro.signals
'''
@pytest.fixture
def venda(cliente, lista_de_produtos):
    venda = Venda.objects.create(
        data=timezone.localdate(),
        cliente=cliente,
        parcelas=6,
        valor=1200
    )
    for produto in lista_de_produtos:
        venda.produtos.add(produto)
    return venda

''' Gerar despesas:
1. Despesa variável
2. Despesa fixa (mensal) sem encerramento
3. Despesa fixa (anual) com encerramento
4. Despesa fixa (mensal) com encerramento
'''
@pytest.fixture
def lista_de_despesas(db):
    return [
        Despesa.objects.create(data=timezone.localdate(), categoria='Motoboy', valor=150),
        Despesa.objects.create(data=timezone.localdate(), categoria='MEI', valor=50, repetir='m'),
        Despesa.objects.create(
            data=timezone.localdate() - relativedelta(years=1),
            data_de_encerramento=timezone.localdate() + relativedelta(months=1),
            categoria='Domínio', valor=95, repetir='a', encerrada=True),
        Despesa.objects.create(
            data=timezone.localdate() - relativedelta(years=1, months=3),
            data_de_encerramento=timezone.localdate() + relativedelta(months=3),
            categoria='Conta de Luz', valor=200, repetir='m', encerrada=True),
    ]
    
@pytest.fixture
def lista_de_materiais(db):
    return [
        Material.objects.create(nome='Esmeralda', entrada=timezone.localdate(), categoria='Pedra', qualidade=5, estoque=3, unidades_compradas=3, valor=1000,),
        Material.objects.create(nome='Diamante', entrada=timezone.localdate(), categoria='Pedra', qualidade=8, estoque=3, unidades_compradas=3, valor=75000,),
        Material.objects.create(nome='Ouro', entrada=timezone.localdate(), categoria='Metal', qualidade=7, estoque=1, unidades_compradas=3, valor=1000,),
    ]

@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(nome='Zé Comédia')

@pytest.fixture
def servico(fornecedor):
    return Servico.objects.create(
        nome='Fotografia',
        data=timezone.localdate(),
        fornecedor=fornecedor,
        qualidade=5,
        valor=100.5
    )

# Visualizar Fluxo de Caixa
@pytest.fixture
def resposta_fluxo_de_caixa(client, lista_de_despesas, venda, lista_de_materiais, servico):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={'ano': timezone.localdate().year, 'mes': timezone.localdate().month})
    )
    return resp

def test_fluxo_de_caixa_status_code(resposta_fluxo_de_caixa):
    assert resposta_fluxo_de_caixa.status_code == 200

# Tabela
def test_despesas_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(resposta_fluxo_de_caixa, despesa.categoria)

def test_parcelas_presente(resposta_fluxo_de_caixa, venda):
    # Formatar parcela -> 1,010.10
    valor = ','.join(str(round(venda.get_valor_parcela(), 2)).split('.'))
    assertContains(resposta_fluxo_de_caixa, valor)

def test_vendas_presente(resposta_fluxo_de_caixa, venda):
    assertContains(resposta_fluxo_de_caixa, venda.cliente.get_nome_completo())

def test_materiais_presente(resposta_fluxo_de_caixa, lista_de_materiais):
    for material in lista_de_materiais:
        assertContains(resposta_fluxo_de_caixa, material.nome)

def test_servico_presente(resposta_fluxo_de_caixa, servico):
    assertContains(resposta_fluxo_de_caixa, servico.nome)

def test_saldo_presente(resposta_fluxo_de_caixa):
    ld = timezone.localdate()
    receitas = Parcela.objects.filter(
        data__month=ld.month, data__year=ld.year).aggregate(Sum('valor'))['valor__sum']
    despesas_variaveis = Despesa.objects.filter(
        repetir='', data__month=ld.month, data__year=ld.year
        ).aggregate(Sum('valor'))['valor__sum']
    despesas_mensais = Despesa.objects.filter(
        Q(encerrada=False) | Q(data_de_encerramento__gte=f'{ld.year}-{ld.month}-{monthrange(ld.year, ld.month)[1]}'),
        data__month__lte=ld.month, data__year__lte=ld.year, repetir='m',
        ).aggregate(Sum('valor'))['valor__sum']
    despesas_anuais = Despesa.objects.filter(
        Q(encerrada=False) | Q(data_de_encerramento__gte=f'{ld.year}-{ld.month}-{monthrange(ld.year, ld.month)[1]}'),
        data__month=ld.month, data__year__lte=ld.year, repetir='a',
        ).aggregate(Sum('valor'))['valor__sum']
    despesas = float(sum([despesas_variaveis, despesas_mensais, despesas_anuais]))
    saldo = float(receitas) - despesas
    # Formatação -> 1,010.00
    saldo_split = f"{saldo:,.1f}".split('.')
    saldo_int = saldo_split[0].replace(',','.')
    saldo_str = ','.join([saldo_int, saldo_split[1]])
    assertContains(resposta_fluxo_de_caixa, saldo_str)

# Gráfico
def test_grafico_correto(resposta_fluxo_de_caixa):
    dados = [0 for i in range(12)]
    ano = timezone.localdate().year
    # Receitas
    receitas = Parcela.objects.filter(data__year=ano).annotate(
        mes=TruncMonth('data')).values('mes').annotate(valor=Sum('valor'))
    for receita in receitas:
        index = receita['mes'].month - 1
        dados[index] += float(receita['valor'])
    # Despesas
    despesas_variaveis = Despesa.objects.filter(repetir='', data__year=ano)
    despesas_mensais = Despesa.objects.filter(
        Q(encerrada=False) | Q(data_de_encerramento__year__gte=ano),
        repetir='m', data__year__lte=ano)
    despesas_anuais = Despesa.objects.filter(
        Q(encerrada=False) | Q(data_de_encerramento__year__gte=ano),
        repetir='a', data__year__lte=ano)
    despesas = [despesas_anuais, despesas_mensais, despesas_variaveis]
    for qs in despesas:
        for despesa in qs:
            index = despesa.data.month - 1
            if despesa.repetir == 'm':
                for i in range(index, 12):
                    dados[i] -= float(despesa.valor)
            else:
                dados[index] -= float(despesa.valor)
    assert resposta_fluxo_de_caixa.context['dados'] == dados

def test_repeticao_mensal_encerrada(client, lista_de_despesas):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={
            'ano': timezone.localdate().year,
            'mes': timezone.localdate().month + 4
        }
    ))
    assertNotContains(resp, Despesa.objects.get(categoria='Conta de Luz'))

def test_repeticao_anual_encerrada(client, lista_de_despesas):
    User.objects.create_user(username='TestUser', password='MinhaSenha123')
    client.login(username='TestUser', password='MinhaSenha123')
    resp = client.get(
        reverse('financeiro:fluxo_de_caixa',
        kwargs={
            'ano': timezone.localdate().year,
            'mes': timezone.localdate().month + 2
        }
    ))
    assertNotContains(resp, Despesa.objects.get(categoria='Domínio'))

# Botões
def test_btn_nova_despesa_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("financeiro:nova_despesa")}'
    )

def test_btn_nova_venda_presente(resposta_fluxo_de_caixa):
    assertContains(
        resposta_fluxo_de_caixa,
        f'href="{reverse("vendas:nova_venda")}'
    )

def test_btn_visualizar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'<a href="#ModalVisualizarDespesa{despesa.id}'
        )

def test_btn_visualizar_venda_presente(resposta_fluxo_de_caixa, venda):
    assertContains(
        resposta_fluxo_de_caixa, f'<a href="#ModalVisualizarVenda{venda.id}'
    )

def test_btn_visualizar_material_presente(resposta_fluxo_de_caixa, lista_de_materiais):
    for material in lista_de_materiais:
        assertContains(
            resposta_fluxo_de_caixa, f'<a href="#ModalVisualizarMaterial{material.despesa.id}'
        )

def test_btn_visualizar_servico_presente(resposta_fluxo_de_caixa, servico):
    assertContains(
        resposta_fluxo_de_caixa, f'<a href="#ModalVisualizarServico{servico.despesa.id}'
    )

def test_btn_editar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'<a href="{reverse("financeiro:editar_despesa", kwargs={"despesa_id": despesa.id})}'
        )

def test_btn_deletar_despesa_presente(resposta_fluxo_de_caixa, lista_de_despesas):
    for despesa in lista_de_despesas:
        assertContains(
            resposta_fluxo_de_caixa, f'<form action="{reverse("financeiro:deletar_despesa", kwargs={"despesa_id": despesa.id})}'
        )

def test_btn_editar_venda_presente(resposta_fluxo_de_caixa, venda):
    assertContains(
        resposta_fluxo_de_caixa, f'<a href="{reverse("vendas:editar_venda", kwargs={"venda_id": venda.id})}'
    )

def test_btn_deletar_venda_presente(resposta_fluxo_de_caixa, venda):
    assertContains(
        resposta_fluxo_de_caixa, f'<form action="{reverse("vendas:deletar_venda", kwargs={"venda_id": venda.id})}'
    )

def test_btn_editar_servico_presente(resposta_fluxo_de_caixa, servico):
    assertContains(
        resposta_fluxo_de_caixa, f'<a href="{reverse("fornecedores:editar_servico", kwargs={"servico_id": servico.id})}'
    )

def test_btn_deletar_servico_presente(resposta_fluxo_de_caixa, servico):
    assertContains(
        resposta_fluxo_de_caixa, f'<form action="{reverse("fornecedores:deletar_servico", kwargs={"servico_id": servico.id})}'
    )
