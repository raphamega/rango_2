from django.urls import path
from .views import *

app_name = 'home'


urlpatterns = [
    path('', home_page, name='home_page'),
    path('about/', about_page, name='sobre'),
    path('aboutl/', loja_about_page, name='loja_sobre'),
    path('contact/', contact_page, name='contato'),
    path('contactl/', loja_contact_page, name='loja_contato'),
]