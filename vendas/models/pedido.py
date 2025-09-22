from django.db import models
from contas.models.cliente import Cliente
from contas.models.endereco import Endereco
from comprar.models.item import Item

class Pedido(models.Model):
    usuario = models.OneToOneField(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    itens = models.ManyToManyField(Item, blank=True, null=True, default=None, related_name='itens_pedido')
    data_venda = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, blank=True, default="PENDENTE")
    valor_total = models.DecimalField(max_digits=7, decimal_places=2)
    valor_subtotal = models.DecimalField(max_digits=7, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=7, decimal_places=2)
    endereco_entrega = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    #FORMA DE PAGAMENTO
