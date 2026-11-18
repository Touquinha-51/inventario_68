from rest_framework import serializers
from .models import Projeto


class ProjetoSerializer(serializers.ModelSerializer):


    class Meta:

        model = Projeto

        fields = [
            "usuario",
            "nome",
            "imagem",
            "descricao",
            "ativo"
        ]

        read_only_fields = ["criado_em"]