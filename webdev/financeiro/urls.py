from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('fluxo_de_caixa/<int:ano>/<int:mes>/', views.fluxo_de_caixa, name='fluxo_de_caixa'),
    # Receitas
    path('receitas/', views.receitas, name='receitas'),
    path('nova_receita/', views.nova_receita, name='nova_receita'),
    path('editar_receita/<int:receita_id>', views.editar_receita, name='editar_receita'),
    path('deletar_receita/<int:receita_id>', views.deletar_receita, name='deletar_receita'),
    # Despesas
    path('despesas/', views.despesas, name='despesas'),
    path('nova_despesa/', views.nova_despesa, name='nova_despesa'),
    path('editar_despesa/<int:despesa_id>', views.editar_despesa, name='editar_despesa'),
    path('deletar_despesa/<int:despesa_id>', views.deletar_despesa, name='deletar_despesa'),
    path('exportar_despesas/', views.exportar_despesas, name='exportar_despesas'),
    path('importar_despesas/', views.importar_despesas, name='importar_despesas'),
]