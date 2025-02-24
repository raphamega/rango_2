from django.urls import path
from .views import Produto_Detalhe, produto_list, adicionar_Produto,editar_produto,Produto_Delete


app_name="produto"

urlpatterns = [
    path("", produto_list, name="produto_list"),
    path("create/", adicionar_Produto, name="produto_add"),
    path("<int:pk>detail/", Produto_Detalhe.as_view(), name="produto_detail"),
    path("<int:pk>edit/", editar_produto, name="produto_edit"),
    path("<int:pk>delet/", Produto_Delete.as_view(), name="produto_delete")
]
