from ..models import models

class Endereco(models.Model):
    cep = models.CharField(max_length=8, blank=False, null=False)
    lagradouro = models.CharField(max_length=100, blank=False, null=False)
    numero = models.CharField(max_length=7, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=False, null=False)
    cidade = models.CharField(max_length=50, blank=False, null=False)
    estado = models.CharField(max_length=25, blank=False, null=False)
    pais = models.CharField(max_length=50, blank=False, null=False, default="BRASIL")
    apelido = models.CharField(max_length=20, blank=False, null=False, default="CASA")
    # Poderia ter Ponto de Referência.

    def __str__(self):
        return f"{self.apelido} | {self.lagradouro} - {self.bairro} - {self.numero}"
