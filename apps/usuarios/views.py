# 1. padrão Python
from functools import wraps
import random

# 2. Django / terceiros
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.urls import reverse

# 3. locais
from .models import Usuario
from .forms import (
    LoginForm,
    RegistroForm,
    UsuarioAdminForm,
    UsuarioMudarEmailForm,
    UsuarioMudarNomeForm
)

def home(request):
    #projetos = Projeto.objects.all() # mesmo o usuario não estando logado, ele vai ter acesso aos projetos
    #if request.user.is_authenticated:
        #meus_projetos = request.user.projetos.all()
        #return render(request, "home.html", {"projetos": projetos, "meus_projetos": meus_projetos}) # quando logado, a view consegue identificar os projetos do usuário e exibí-los
    #else:
        #return render(request, "home.html", {"projetos": projetos}) # quando não logado, a view exibe todos os projetos
    return render(request, "home.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("/home")

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "/home"))
            else:
                messages.error(request, "Credenciais inválidas.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# view de logout
def logout(request):
    # encerra a sessão
    logout(request)
    # redireciona para login
    return redirect("login.html")