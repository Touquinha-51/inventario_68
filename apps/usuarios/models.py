from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager


# Gerenciador para lidar com a criação de usuários sem o campo 'username'
class UsuarioManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):

    username = None  # removendo o username porque não vamos usá-lo
    email = models.EmailField(primary_key=True, unique=True)  # só um email por usuário
    nome = models.CharField(max_length=100, blank=False, null=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    codigo_verificacao = models.CharField(max_length=4, blank=True, null=True)
    codigo_expira_em = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Define o campo de email como o campo de identificação do usuário
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()  # Usando o gerenciador personalizado para lidar com a criação de usuários

    @property
    def is_admin_user(self):
        return self.is_staff or self.is_superuser
    

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        ordering = ["criado_em"]

    def __str__(self):
        return f"{self.nome} {self.email}"
