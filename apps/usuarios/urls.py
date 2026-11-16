from django.urls import path

from . import views

urlpatterns = [
    path("criar_conta/", views.criar_conta, name="criar_conta"),
    path("login/", views.funcao_login, name="login"),
    path("logout/", views.funcao_logout, name="logout"),
    path("confirmar_codigo/", views.confirmar_codigo, name="confirmar_codigo"),
    path("reenviar_codigo/", views.reenviar_codigo, name="reenviar_codigo"),
    path("mudar_nome/", views.mudar_nome, name="mudar_nome"),
    path("mudar_email/", views.mudar_email, name="mudar_nome"),
    path("confirmar_novo_email", views.confirmar_novo_email, name="confirmar_novo_email")
]
