from django.urls import path

from . import views

urlpatterns = [
    path("criar_projeto/", views.criar_projeto, name="criar_projeto"),
    path("editar_projeto/", views.editar_projeto, name="editar_projeto"),
    path("excluir_projeto", views.excluir_projeto, name="excluir_projeto")
]
