from django.urls import path

from . import views

urlpatterns = [
    path("criar_projeto/", views.criar_projeto, name="criar_projeto"),
]
