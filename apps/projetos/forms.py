from .models import Projeto
from django import form


class CriarProjeto(models.ModelForm):


    class Meta:
        models = Projeto
        fields = [
            "nome",
            "descricao",
            "imagem",
        ]