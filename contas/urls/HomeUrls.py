from django.urls import path
from contas.views.HomeView import home_view, sair_view, logar_view, cadastrar_view

urlpatterns = [
    path('', home_view, name='inicio'),
    path('login/', logar_view, name='logar'),
    path('cadastrar/', cadastrar_view, name='cadastrar'),
    path('sair/', sair_view, name='sair'),
]