from django.urls import path

from . import views

app_name = "apps.usuarios"

urlpatterns = [
    #path("criar_conta/", views.criar_conta, name="criar_conta"),
    path("login/", views.login, name="login"),
    #path("codigo_confirmacao/", views.verificar_codigo, name="verificar_codigo")
]
