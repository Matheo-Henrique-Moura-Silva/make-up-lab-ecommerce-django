from django.db import models

class Galeria(models.Model):
    imagem = models.ImageField(upload_to='produtos/galerias/')
