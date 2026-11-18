from django.db import models
from apps.usuarios.models import Usuario
from apps.itens.models import Item


class Projeto(models.Model):

    nome = models.CharField(max_length=60, blank=False, null=False)
    descricao = models.TextField(max_length=200, blank=False, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="projetos/", blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    itens = models.ManyToManyField(Item, through="ProjetoItem")

    def __str__(self):
        return f"{self.nome} - {self.usuario}"


class ProjetoItem(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.PositiveSmallIntegerField(default=0)