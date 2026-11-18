from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    tipo = models.CharField(max_length=50, blank=False, null=False)
    imagem = models.ImageField(upload_to="projetos/", blank=True, null=True)
    descricao = models.TextField(max_length=200, blank=False, null=False)
    quantidade_total = models.PositiveSmallIntegerField(default=0)
    
    @property
    def quantidade_em_uso(self):
        soma = 0
        for objeto in self.projetoitem_set.all():
            soma += objeto.quantidade

    @property
    def quantidade_disponivel(self):
        return self.quantidade_total - self.quantidade_em_uso
    
    def __str__(self):
        return f"{self.nome}"
