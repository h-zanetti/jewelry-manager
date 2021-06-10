from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.minhas_vendas, name='minhas_vendas'),
    path('nova_venda/', views.nova_venda, name='nova_venda'),
    path('editar_venda/<int:venda_id>', views.editar_venda, name='editar_venda'),
    path('deletar_venda/<int:venda_id>', views.deletar_venda, name='deletar_venda'),
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('novo_cliente/', views.novo_cliente, name='novo_cliente'),
    path('editar_cliente/<int:cliente_id>', views.editar_cliente, name='editar_cliente'),
    path('deletar_cliente/<int:cliente_id>', views.deletar_cliente, name='deletar_cliente'),
]