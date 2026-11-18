from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProjetoViewSet

router = DefaultRouter()
router.register(r'', ProjetoViewSet, basename='projetos')

urlpatterns = [
    path('', include(router.urls)),
]