from django.db import models
from apps.usuarios.models import Usuario


class Projeto(models.Model):

    nome = models.CharField(max_length=60)
    descricao = models.TextField(max_length=200, blank=False, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="projetos/", blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.usuario}"