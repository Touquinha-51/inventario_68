from rest_framework import serializers
from .models import Usuario
from .services.usuario_service import UsuarioService


# serializer principal para leitura de usuários
class UsuarioSerializer(serializers.ModelSerializer):
    # campo extra apenas para exibição do tipo
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = Usuario
        # campos expostos na api
        fields = [
            "id",
            "nome",
            "email",
            "tipo",
            "tipo_display",
            "is_active",
            "criado_em",
        ]
        # campos somente leitura (não podem ser alterados via api)
        read_only_fields = ["criado_em"]


# serializer usado apenas na criação de usuários
class UsuarioCreateSerializer(serializers.ModelSerializer):
    # senha principal (não retorna na api)
    senha = serializers.CharField(write_only=True, min_length=8)
    # confirmação de senha
    senha_confirmacao = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        # campos permitidos na criação
        fields = [
            "nome",
            "email",
            "senha",
            "senha_confirmacao",
        ]

    # validação personalizada para garantir que as senhas coincidem
    def validate(self, attrs):
        if attrs["senha"] != attrs["senha_confirmacao"]:
            raise serializers.ValidationError({"senha_confirmacao": "as senhas não coincidem."})
        return attrs

    # criação do usuário delegada para a camada de serviço
    def create(self, validated_data):
        # remove confirmação de senha antes de criar
        validated_data.pop("senha_confirmacao")

        # chama o service (regra de negócio centralizada)
        return UsuarioService.criar_usuario(validated_data)