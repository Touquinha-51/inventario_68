from django.db import models
from .models import Usuario


class Projeto(models.Model):

    nome = models.CharField(max_lenght=60)
    descricao = models.TextField(max_lenght=200, Blank=False, Null=False)
    usuario = models.ForeignKey(Usuario, on_delete.CASCADE)
    imagem = models.ImageField(upload_to="projetos/", Blank=True, Null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.usuario}"