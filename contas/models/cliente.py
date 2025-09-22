from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import models, Usuario, endereco

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    aniversario = models.DateField(default=None, null=True, blank=True)
    # Implementar carrinho de compras;
    # Implementar forma de pagamento;
    enderecos = models.ManyToManyField(endereco.Endereco, blank=True, default=None, related_name='lista_de_enderecos')
    # Para acessar "cliente.enderecos.all()"

    def __str__(self):
        return self.usuario.get_full_name()

    @receiver(post_save, sender=Usuario)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Cliente.objects.create(usuario=instance)
