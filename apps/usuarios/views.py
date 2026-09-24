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
from .services.usuario_service import UsuarioService
from .forms import (
    LoginForm,
    RegistroForm,
    UsuarioAdminForm,
    UsuarioUpdateEmailForm,
    UsuarioUpdateNomeForm
)

def home(request):
    projetos = Projetos.objects.all() # mesmo o usuario não estando logado, ele vai ter acesso aos projetos
    if request.user.is_authenticated:
        meus_projetos = request.user.projetos.all()
        return render(request, "home.html", {"projetos": projetos, "meus_projetos": meus_projetos}) # quando logado, a view consegue identificar os projetos do usuário e exibí-los
    else:
        return render(request, "home.html", {"projetos": projetos}) # quando não logado, a view exibe todos os projetos

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
def logout_view(request):
    # encerra a sessão
    logout(request)
    # redireciona para login
    return redirect("login.html")

# view de registro
def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            codigo_verificacao = str(random.randint(1000, 9999))

            request.session['dados_registro_pendente'] = {
                'email': dados['email'],
                'password': dados['password1'],
                'codigo': codigo_verificacao
            }

            request.session['usuario_verificando_id'] = True

            print(f"Código para {dados['email']}: {codigo_verificacao}")
            return redirect('apps.usuarios:verificar_codigo')

        # Se o form for INVÁLIDO, ele cai aqui (ainda no POST)
        return render(request, 'criar_conta.html', {'form': form})

    form = RegistroForm()
    return render(request, 'criar_conta.html', {'form': form})

def verificar_codigo(request):
    if not request.session.get('usuario_verificando_id'):
        return redirect("apps.usuarios:registrar")

    if request.method == "POST":
        # .strip() remove espaços acidentais e str() garante a tipagem
        codigo_digitado = str(request.POST.get("codigo", "")).strip()
        dados = request.session.get('dados_registro_pendente')

        if dados and codigo_digitado == str(dados.get('codigo')):
            try:
                UsuarioService.criar_usuario({
                    'email': dados['email'],
                    'password': dados['password'],
                    'is_active': True
                })

                # Limpeza segura
                request.session.pop('usuario_verificando_id', None)
                request.session.pop('dados_registro_pendente', None)

                messages.success(request, "Conta criada com sucesso!")
                return redirect("/usuarios/login/")  # O esperado 302

            except Exception as e:
                messages.error(request, f"Erro no Service: {e}")
        else:
            # Se cair aqui, a View retorna 200 e o teste falha
            messages.error(request, "Código inválido.")

    return render(request, "verificador.html")

def criar_projeto(request):
    if request.user.is_authenticated:
        if request.method == "GET":



def editar_projeto(request):



def excluir_projeto(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id_projeto = request.POST.get("id_projeto")
            projeto = get_object_or_404(Projeto, id_projeto=id_projeto)
            if request.user.is_staff or projeto.usuario == request.user:
                projeto.delete()
                messages.success(request, "Projeto excluído com sucesso")
            else:
                messages.error(request, "Você não possuí permissão para executar esta ação")

        return redirect("home.html")

    else:
        messages.error("Faça o seu login antes")
        return redirect("login.html")
        