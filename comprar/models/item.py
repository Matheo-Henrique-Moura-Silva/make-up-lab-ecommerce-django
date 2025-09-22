from django.db import models
from adminSite.models.produto import Produto

class Item(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens_criados')
    quantidade = models.IntegerField(default=1)

    def set_quantidade(self, qtnd):
        self.quantidade = qtnd

    def get_valor(self):
        valor = self.produto.preco * self.quantidade
        return valor
