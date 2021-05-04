from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.estoque, name='estoque_produtos'),
    path('novo/', views.novo_produto, name='novo_produto'),
    path('editar/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('deletar/<int:produto_id>', views.deletar_produto, name='deletar_produto'),
]