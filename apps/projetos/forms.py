from .models import Projeto
from django import forms
from django.db import models


class CriarProjeto(forms.ModelForm):


    class Meta:
        models = Projeto
        fields = [
            "nome",
            "descricao",
            "imagem",
        ]