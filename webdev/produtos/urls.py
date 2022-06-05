from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Produto
    path('', views.estoque, name='estoque_produtos'),
    path('categorias/', views.categorias, name='categorias'),
    path('novo/', views.novo_produto, name='novo_produto'),
    path('actions/', views.product_action_page, name='product_actions'),
    path('product_barcode/', views.product_barcode, name='product_barcode'),
    path('editar/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('deletar/<int:produto_id>', views.deletar_produto, name='deletar_produto'),
    path('duplicar/<int:produto_id>', views.duplicar_produto, name='duplicar_produto'),
    # Serviço
    path('adicionar_servico/<int:produto_id>', views.adicionar_servico, name='adicionar_servico'),
    path('editar_servico_dp/<int:servico_dp_id>', views.editar_servico_dp, name='editar_servico_dp'),
    path('remover_servico_dp/<int:servico_dp_id>', views.remover_servico_dp, name='remover_servico_dp'),
    # Material
    path('adicionar_material/<int:produto_id>', views.adicionar_material, name='adicionar_material'),
    path('editar_material_dp/<int:material_dp_id>', views.editar_material_dp, name='editar_material_dp'),
    path('remover_material_dp/<int:material_dp_id>', views.remover_material_dp, name='remover_material_dp'),
    # Importação e exportação
    path('exportar/', views.exportar_produtos, name='exportar_produtos'),
    path('importar/', views.importar_produtos, name='importar_produtos'),
]