from django.contrib import admin
from django.urls import path
from adminSite.views.AdminView import admin_view, dashboard_view, sair_admin_view, produtos_view, excluir_produto_view, editar_produto_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_view, name='entrar'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('sairadmin/', sair_admin_view, name='sairadm'),
    path('produtos/', produtos_view, name='produtos'),
    path('excluir_produto/<int:id>', excluir_produto_view, name='excluir_produto'),
    path('editar_produto/<int:id>', editar_produto_view, name='editar_produto'),
]
