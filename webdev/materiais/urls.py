from django.urls import path
from . import views

app_name = 'materiais'

urlpatterns = [
    # Estoque
    path('', views.estoque_materiais, name='estoque_materiais'),
    path('cadastrar_material/', views.cadastrar_material, name='cadastrar_material'),
    path('editar_material/<int:material_id>/', views.editar_material, name='editar_material'),
    path('deletar_material/<int:material_id>/', views.deletar_material, name='deletar_material'),
    path('exportar_material/', views.exportar_materiais, name='exportar_materiais'),
    path('importar_material/', views.importar_materiais, name='importar_materiais'),
    # Entradas
    path('entrada_de_material/', views.entrada_de_material, name='entrada_de_material'), # Formulário de entrada de material
    path('entradas_de_materiais/', views.entradas_de_materiais, name='entradas_de_materiais'), # Lista de entradas de materiais
    path('editar_entrada/<int:entrada_id>/', views.editar_entrada, name='editar_entrada'),
    path('deletar_entrada/<int:entrada_id>/', views.deletar_entrada, name='deletar_entrada'),
    path('exportar_entradas/', views.exportar_entradas, name='exportar_entradas'),
    path('importar_entradas/', views.importar_entradas, name='importar_entradas'),
]