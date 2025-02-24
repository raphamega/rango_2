from django.urls import path
from .views import *

app_name = 'estoque'

urlpatterns = [
    path('', estoque_lista, name='estoque_list'),
    path("<int:pk>detail/", Estoque_Detalhe.as_view(), name="estoque_detail"),
    path('move/', estoque_movimento, name='estoque_move'),
    path('abrir/', nota_abrir, name='nota_abrir'),
    path('<int:pk>item/', adcionar_item, name='estoque_add'),
    path('item_del', excluir_item, name='excluir_item'),
    path('nota/', gerar_nota, name='gerar_nota'),
    path('delete/', excluir_nota, name='excluir_nota'),
]
