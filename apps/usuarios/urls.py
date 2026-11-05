from django.urls import path

from . import views

urlpatterns = [
    path("criar_conta/", views.criar_conta, name="criar_conta"),
    path("login/", views.login, name="login"),
    path("confirmar_codigo/", views.confirmar_codigo, name="confirmar_codigo")
    path("reenviar_codigo/", views.reenviar_codigo, name="reenviar_codigo")
]
