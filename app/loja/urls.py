from django.urls import path, reverse_lazy
from django.contrib.auth.views import *
from .views import *

app_name = "loja"

urlpatterns = [
    path('', loja_home, name='loja_home'),
    path('loja/', Loja_Update.as_view(), name='loja_update'),
    # path('loja/', gerarLoja, name='loja_update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('usuario:login')), name='logout'),
    path('registrar/', gerarUsuario, name='user-create'),
    path('update/', gerarPerfil, name='user-update'),

]
