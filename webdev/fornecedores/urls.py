from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    # Fornecedor
    path('', views.meus_fornecedores, name='meus_fornecedores'),
    path('novo/', views.novo_fornecedor, name='novo_fornecedor'),
    path('editar/<int:fornecedor_id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('deletar/<int:fornecedor_id>/', views.deletar_fornecedor, name='deletar_fornecedor'),
    # Fornecimento
    path('novo_fornecimento/<int:fornecedor_id>/', views.novo_fornecimento, name='novo_fornecimento'),
    path('editar_fornecimento/<int:fornecimento_id>/', views.editar_fornecimento, name='editar_fornecimento'),
    path('deletar_fornecimento/<int:fornecimento_id>/', views.deletar_fornecimento, name='deletar_fornecimento'),
    # Email
    path('novo_email/<int:fornecedor_id>/', views.novo_email, name='novo_email'),
    path('editar_email/<int:email_id>/', views.editar_email, name='editar_email'),
    path('deletar_email/<int:email_id>/', views.deletar_email, name='deletar_email'),
    # Telefone
    path('novo_telefone/<int:fornecedor_id>/', views.novo_telefone, name='novo_telefone'),
    path('editar_telefone/<int:telefone_id>/', views.editar_telefone, name='editar_telefone'),
    path('deletar_telefone/<int:telefone_id>/', views.deletar_telefone, name='deletar_telefone'),
    # Localização
    path('novo_local/<int:fornecedor_id>/', views.novo_local, name='novo_local'),
    path('editar_local/<int:local_id>/', views.editar_local, name='editar_local'),
    path('deletar_local/<int:local_id>/', views.deletar_local, name='deletar_local'),
    # Dados Bancários
    path('novos_dados_bancarios/<int:fornecedor_id>/', views.novos_dados_bancarios, name='novos_dados_bancarios'),
    path('editar_dados_bancarios/<int:dados_bancarios_id>/', views.editar_dados_bancarios, name='editar_dados_bancarios'),
    path('deletar_dados_bancarios/<int:dados_bancarios_id>/', views.deletar_dados_bancarios, name='deletar_dados_bancarios'),
    # Serviços
    path('novo_servico/', views.novo_servico, name='novo_servico'),
    path('editar_servico/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('deletar_servico/<int:servico_id>/', views.deletar_servico, name='deletar_servico'),
]