"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from apps.usuarios.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("usuarios/", include("apps.usuarios.urls")),
    #path("projetos/", include("apps.projetos.urls")),
    #path("itens/", include("apps.itens.urls")),

    #caminho dos endpoints da API
    #path("api/usuarios/", include("apps.usuarios.api_urls")),
    #path("api/projetos/", include("apps.projetos.api_urls")),
    #path("api/itens/", include("apps.itens.api_urls")),
]
