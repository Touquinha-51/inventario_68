from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    username = None  # removendo o username porque não vamos usá-lo
    email = models.EmailField(unique=True)  # só um email por usuário
    nome = models.CharField(max_length=100, blank=False, null=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    codigo_verificacao = models.CharField(max_length=4, blank=True, null=True)
    codigo_expira_em = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Define o campo de email como o campo de identificação do usuário
    REQUIRED_FIELDS = ['nome']

    @property
    def is_admin_user(self):
        return self.is_staff or self.is_superuser


    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        ordering = ["criado_em"]

    def __str__(self):
        return f"{self.nome} {self.email}"
    