from django.db import models
from contas.models.cliente import Cliente
from .item import Item

class Carrinho(models.Model):
    usuario = models.OneToOneField(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    itens = models.ManyToManyField(Item, blank=True, null=True, default=None, related_name='itens_carrinho')
    is_ativo = models.BooleanField(default=True)
    valor_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    itens_total = models.IntegerField(default=0)

    def adicionar_item(self, item_id):
        item = Item.objects.get(id=item_id)
        self.itens.add(item)
        self.valor_total = self.get_valor()
        self.itens_total = self.get_total_itens()
        return True

    def remover_item(self, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except:
            return False
        else:
            self.itens.remove(item)
            item.delete()
            self.valor_total = self.get_valor()
            self.itens_total = self.get_total_itens()
            return True

    def limpar(self):
        for item in self.itens.all():
            item.delete()
        self.itens.clear()
        self.valor_total = self.get_valor()
        self.itens_total = self.get_total_itens()

    def get_valor(self):
        valor = 0
        for item in self.itens.all():
            valor += item.get_valor()
        return valor

    def get_total_itens(self):
        qntd = 0
        for item in self.itens.all():
            qntd += 1
        return qntd

    def is_vazio(self):
        if self.itens.count() == 0:
            return True
        else:
            return False

    def set_is_ativo(self):
        self.is_ativo = False

    def produto_existe(self, id):
        for item in self.itens.all():
            if item.produto.id == id:
                return True
        return False

    def get_qntd_item(self, id):
        for item in self.itens.all():
            if item.produto.id == id:
                return item.quantidade

    def gerar_pedido(self):
        pass
