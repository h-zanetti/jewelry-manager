from django.urls import path
from . import views

app_name = 'materiais'

urlpatterns = [
    path('', views.estoque_materiais, name='estoque_materiais'),
    path('nova_entrada/', views.nova_entrada, name='nova_entrada'),
    path('editar_material/<int:material_id>/', views.editar_material, name='editar_material'),
    path('deletar_material/<int:material_id>/', views.deletar_material, name='deletar_material'),
]