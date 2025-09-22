from django.urls import path
from comprar.views.ComprarView import *

urlpatterns = [
    path('ver_produto/<int:id>', ver_produto, name='ver_produto'),
    path('ver_produto/<int:id>/adicionar_item_carrinho/<int:qntd>', adicionar_item_carrinho, name='adicionar_item_carrinho'),
    path('ver_carrinho/', ver_carrinho,name='ver_carrinho'),
    path('ver_carrinho/remover_item_carrinho/<int:id>', remover_item_carrinho, name='remover_item_carrinho'),
    path('ver_carrinho/editar_item_carrinho/<int:id>/<int:qntd>', editar_item_carrinho, name='editar_item_carrinho'),
    path('ver_carrinho/limpar_carrinho/<int:id>', limpar_carrinho, name='limpar_carrinho'),
    path('adicionar_produto_favorito/<int:id>', adicionar_produto_favorito, name='adicionar_produto_favorito'),
    path('ver_favoritos/', ver_favoritos, name='ver_favoritos'),
    path('buscar_produto/', buscar_produto, name='buscar_produto'),
]
