from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.estoque, name='estoque_produtos'),
    path('categorias/', views.categorias, name='categorias'),
    path('novo/', views.novo_produto, name='novo_produto'),
    path('editar/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('deletar/<int:produto_id>', views.deletar_produto, name='deletar_produto'),
    path('adicionar_servico/<int:produto_id>', views.adicionar_servico, name='adicionar_servico'),
    path('adicionar_material/<int:produto_id>', views.adicionar_material, name='adicionar_material'),
    path('editar_material_dp/<int:material_dp_id>', views.editar_material_dp, name='editar_material_dp'),
    path('remover_material_dp/<int:material_dp_id>', views.remover_material_dp, name='remover_material_dp'),
]