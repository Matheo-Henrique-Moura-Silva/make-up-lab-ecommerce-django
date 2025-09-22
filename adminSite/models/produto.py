from adminSite.models import categoria, marca, galeria
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=30, blank=True)
    descricao = models.CharField(max_length=200, blank=False)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    custo = models.DecimalField(max_digits=7, decimal_places=2)
    estoque = models.IntegerField(default=0)
    categoria = models.ForeignKey(categoria.Categoria, on_delete=models.SET_NULL, blank=True, null=True, related_name='lista_produtos')
    marca = models.ForeignKey(marca.Marca, on_delete=models.SET_NULL, blank=True, null=True, related_name='lista_produtos')
    imagem_capa = models.ImageField(upload_to='produtos/capas/', blank=True, null=True)
    galeria_imagem = models.ForeignKey(galeria.Galeria, on_delete=models.SET_NULL, blank=True, null=True, related_name='lista_produtos')

    def __str__(self):
        return self.nome
