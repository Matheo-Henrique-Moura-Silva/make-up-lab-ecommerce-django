from django.db import models

class Marca(models.Model):
    nome = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nome
