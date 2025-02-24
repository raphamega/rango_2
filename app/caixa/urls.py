from django.urls import path
from .views import *

app_name = "caixa"


urlpatterns = [
    path('', caixa_home, name='caixa_home'),
    path('registra', caixa_add, name='caixa_add'),
    path('registradora-<int:pk>/', registradora_home, name='registradora_home'),
    path('<int:pk>/item', registradora_item, name='registradora_Item'),
    path('busca-<int:pk>', busca_produto, name='query'),
    path('obs', observacao, name='observacao'),
    path('delete', registradora_remover_item, name='registradora_remove'),
    path('acres', registradora_acrecimo, name='registradora_acrescimo'),
    path('<int:pk>/acrescimo_list', acrescimo_list, name='acrescimo_list'),
    path('<int:pk>/enviado', registradora_pedido, name='registradora_pedido'),
    path('<int:pk>/entrega', registradora_entrega, name='registradora_entrega'),
    path('<int:pk>/pagamento', registradora_pagamento, name='registradora_pagamento'),
    path('<int:pk>/enviado_pedido', registradora_aceitar_pedido, name='registradora_aceitar_pedido'),
    path('<int:pk>/balcao', registradora_retirar_balcao, name='registradora_retirar_balcao'),
    path('<int:pk>/mesa', registradora_retirar_mesa, name='registradora_retirar_mesa'),
    path('<int:pk>/fecharmesa', fechar_mesa, name='fechar_mesa'),
    path('<int:pk>/pagamento_mesa', registradora_pagamento_mesa, name='registradora_pagamento_mesa'),
    path('<int:pk>/fechado', registradora_mesa_receber, name="registradora_mesa_receber"),

]