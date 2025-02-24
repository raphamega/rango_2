from django.urls import path
from .views import *

app_name = "pedido"


urlpatterns = [
    path('item/', pedido_item, name='pedido_Item'),
    #path('', pedido_List, name='pedido_list'),
    path('obs', observacao, name='observacao'),
    path('delete', remover_item, name='remove'),
    path('acres', pedido_acrecimo, name='acrescimo'),
    path('<int:pk>/acrescimo_list', acrescimo_list, name='acrescimo_list'),

      #CONTROLE DE MESAS
    path('mesa_lista/', mesa_list, name='mesa_list'),
    path('mesa_criar/', mesa_criar, name='mesa_criar'),
    path('pedido_criar/', pedido_criar, name='pedido_criar'),
    path('<int:pk>_del_ped', pedido_delete, name='pedido_delete'),
    path('<int:pk>del_mesa', mesa_delete, name='mesa_delete'),
    path('<int:pk>ler_pedido', ler_pedido, name='ler_pedido'),
    path('<int:pk>pronto', pedido_pronto, name='pedido_pronto'),
    path('<int:pk>recebido', pedido_recebido, name='pedido_recebido'),
]
