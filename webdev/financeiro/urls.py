from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('fluxo_de_caixa/<int:ano>/<int:mes>/', views.fluxo_de_caixa, name='fluxo_de_caixa'),
    # Despesas
    path('despesas/', views.despesas, name='despesas'),
    path('nova_despesa/', views.nova_despesa, name='nova_despesa'),
    path('editar_despesa/<int:despesa_id>', views.editar_despesa, name='editar_despesa'),
    path('deletar_despesa/<int:despesa_id>', views.deletar_despesa, name='deletar_despesa'),
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('novo_cliente/', views.novo_cliente, name='novo_cliente'),
    path('editar_cliente/<int:cliente_id>', views.editar_cliente, name='editar_cliente'),
    path('deletar_cliente/<int:cliente_id>', views.deletar_cliente, name='deletar_cliente'),
    # Vendas
    path('vendas/', views.vendas, name='vendas'),
    path('nova_venda/', views.nova_venda, name='nova_venda'),
    path('editar_venda/<int:venda_id>', views.editar_venda, name='editar_venda'),
    path('deletar_venda/<int:venda_id>', views.deletar_venda, name='deletar_venda'),
]