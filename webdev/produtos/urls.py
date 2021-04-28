from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.estoque, name='estoque'),
    path('novo', views.novo_produto, name='novo_produto'),
]