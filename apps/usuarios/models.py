from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    class Tipo(models.TextChoices):
        USUARIO = "CIDADAO", "Cidadão"
        ADMIN = "ADMIN", "Administrador"

    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.USUARIO,
        verbose_name="tipo de usuário",
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    codigo_verificacao = models.CharField(max_length=6, blank=True, null=True)
    codigo_expira_em = models.DateTimeField(blank=True, null=True)


    @property
    def is_admin_user(self):
        return self.tipo == self.Tipo.ADMIN


    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    