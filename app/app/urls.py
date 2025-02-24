from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('loja/', include('loja.urls', namespace='loja')),
    path('produto/', include('produto.urls', namespace='produto')),
    path('estoque/', include('estoque.urls', namespace='estoque')),
    path('caixa/', include('caixa.urls', namespace='caixa')),
    path('pedido/', include('pedido.urls', namespace='pedido')),
]
urlpatterns += [path("accounts", include("django.contrib.auth.urls"))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

