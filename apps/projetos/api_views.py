from rest_framework.viewsets import ModelViewSet
from .models import Projeto
from .serializers import ProjetoSerializer


class ProjetoViewSet(ModelViewSet):
    queryset = Projeto.objects.all().order_by("criado_em")
    serializer_class = ProjetoSerializer