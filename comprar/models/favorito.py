from django.db import models
from contas.models.cliente import Cliente
from adminSite.models.produto import Produto

class Favorito(models.Model):
    usuario = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, blank=True, null=True, default=None, related_name='produtos_favoritos')

    def add_favorito(self, id):
        try:
            produto = Produto.objects.get(id=id)
        except:
            return False
        else:
            self.produtos.add(produto)
            return True

    def del_favorito(self, id):
        try:
            produto = Produto.objects.get(id=id)
        except:
            return False
        else:
            self.produtos.remove(produto)
            return True

    def is_vazio(self):
        if self.produtos.count() == 0:
            return True
        else:
            return False

    def clear_favoritos(self):
        if self.is_vazio():
            return False
        else:
            self.produtos.clear()

    def produto_existe(self, id):
        for produto in self.produtos.all():
            if produto.id == id:
                return True
        return False

    def get_usuario(self):
        return self.usuario

    def get_produto(self):
        return self.produto

    def get_todos_favoritos(self):
        return self.produtos.all()
