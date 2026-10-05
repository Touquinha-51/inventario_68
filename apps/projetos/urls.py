from django.urls import path

from . import views

app_name = "apps.projetos"

urlpatterns = [
    path("criar_projeto/", views.criar_projeto, name="criar_projeto"),
]
