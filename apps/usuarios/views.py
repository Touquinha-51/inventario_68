# 1. padrão Python
from functools import wraps
import secrets

# 2. Django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

# 3. locais
from .models import Usuario
from apps.projetos.models import Projeto
from .forms import (
    LoginForm,
    RegistroForm,
    UsuarioAdminForm,
    UsuarioMudarEmailForm,
    UsuarioMudarNomeForm,
    CodigoForm
)

def home(request):
    projetos = Projeto.objects.all() # mesmo o usuario não estando logado, ele vai ter acesso aos projetos
    if request.user.is_authenticated:
        meus_projetos = request.user.projeto_set.all()
        return render(request, "home.html", {"projetos": projetos, "meus_projetos": meus_projetos}) # quando logado, a view consegue identificar os projetos do usuário e exibí-los
    else:
        return render(request, "home.html", {"projetos": projetos}) # quando não logado, a view exibe todos os projetos
    return render(request, "home.html")

def funcao_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                if user.verificado:
                    login(request, user)
                    next_url = request.POST.get("next") or request.GET.get("next")

                    if next_url and url_has_allowed_host_and_scheme(
                        next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure()
                    ):
                        return redirect(next_url)

                    return redirect("home")
                else:
                    messages.error(request, "Sua conta não é verificada.")
            else:
                messages.error(request, "Credenciais inválidas.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

# view de logout
def funcao_logout(request):
    # encerra a sessão
    logout(request)
    return redirect("login")

def criar_conta(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        print("FORMULÁRIO VÁLIDO:", form.is_valid())
        print("ERROS:", form.errors)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.codigo_confirmacao = secrets.randbelow(900000) + 100000
            usuario.codigo_expira_em = timezone.now() + timedelta(minutes=5)
            usuario.save()
            print("USUÁRIO SALVO:", usuario.email)
            request.session["usuario_email"] = usuario.email

            send_mail(
                subject="Confirmação de email - Inventário 68",
                message=f"Seu código de confirmação é: {usuario.codigo_confirmacao}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
            )

            return redirect("confirmar_codigo")

        return render(request, 'criar_conta.html', {'form': form})

    form = RegistroForm()
    return render(request, 'criar_conta.html', {'form': form})

def confirmar_codigo(request):

    email = request.session.get("usuario_email")

    if not email:
        messages.error(request, "Sessão de confirmação não encontrada.")
        return redirect("criar_conta")

    usuario = get_object_or_404(Usuario, email=email)

    if request.method == "POST":
        form = CodigoForm(request.POST)
        if form.is_valid():

             # Verifica se o código ainda existe
            if not usuario.codigo_confirmacao:
                messages.error(request, "Não existe um código válido.")

            # Verifica se o código expirou
            elif (timezone.now() >= usuario.codigo_expira_em):
                usuario.codigo_confirmacao = None
                usuario.codigo_expira_em = None
                usuario.save()

                messages.error(request, "Seu código expirou. Solicite um novo.")
                print(request._messages._queued_messages[-1])

            # Verifica o limite de tentativas
            elif usuario.tentativas >= 10:
                messages.error(request, "Você excedeu o limite de tentativas.")
                print(request._messages._queued_messages[-1])
                print("tentativas:", usuario.tentativas)

            else:
                codigo = form.cleaned_data["codigo"]

                if usuario.codigo_confirmacao == codigo:
                    if Usuario.objects.filter(email=email).exclude(pk=usuario.pk).exists():
                        messages.error(request, "Este email já está cadastrado.")
                    else:
                        usuario.verificado = True
                        usuario.codigo_confirmacao = None
                        usuario.codigo_expira_em = None
                        usuario.tentativas = 0
                        usuario.save()

                        request.session.pop("usuario_email", None)

                        messages.success(request, "Código confirmado, sua conta está pronta para o login.")
                        print(request._messages._queued_messages[-1])

                        return redirect("login")

                else:
                    messages.error(request, "código incorreto")
                    usuario.tentativas += 1
                    usuario.save()
                    print(request._messages._queued_messages[-1])
                    print("tentativas:", usuario.tentativas)
        else:
            messages.error(request, "formulário inválido")
    else:
        form = CodigoForm()
    return render(request, "confirmar_codigo.html", {"form": form})

def reenviar_codigo(request):
    if request.method == "POST":

        email = request.session.get("usuario_email")

        if not email:
            messages.error(request, "Sessão de confirmação não encontrada.")
            return redirect("criar_conta")

        usuario = get_object_or_404(Usuario, email=email)

        if timezone.now() <= usuario.codigo_expira_em:
            messages.error(request, "aguarde o tempo acabar para solicitar um novo código")
            print(request._messages._queued_messages[-1])
            print("acaba em:", usuario.codigo_expira_em)
        else:

            email = request.session.get("usuario_email")

            if not email:
                messages.error(request, "Sessão de confirmação não encontrada.")
                return redirect("criar_conta")

            usuario = get_object_or_404(Usuario, email=email)

            usuario.codigo_confirmacao = secrets.randbelow(900000) + 100000
            usuario.codigo_expira_em = timezone.now() + timedelta(minutes=5)
            usuario.tentativas = 0
            usuario.save()

            send_mail(
                subject="Confirmação de email - Inventário 68",
                message=f"Seu código de confirmação é: {usuario.codigo_confirmacao}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
            )

            messages.success(request, "Código reenviado para o seu email.")

    return redirect("confirmar_codigo")

@login_required
def mudar_nome(request):
    if request.method == "POST":
        form = UsuarioMudarNomeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "nome alterado")
            return redirect("home")
    else:
        form = UsuarioMudarNomeForm(instance=request.user)
    return render(request, "mudar_nome.html", {"form": form})

@login_required
def mudar_email(request):
    if request.method == "POST":
        form = UsuarioMudarEmailForm(request.POST, instance=request.user)
        usuario = request.user
        if form.is_valid():
            usuario.codigo_confirmacao = secrets.randbelow(900000) + 100000
            usuario.codigo_expira_em = timezone.now() + timedelta(minutes=5)
            usuario.save()
            novo_email = form.cleaned_data["email"]
            request.session["novo_email"] = novo_email

            send_mail(
                subject="Confirmação de email - Inventário 68",
                message=f"Seu código de confirmação é: {usuario.codigo_confirmacao}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[novo_email]
            )

            return redirect("confirmar_novo_email")
            
    else:
        form = UsuarioMudarEmailForm(instance=request.user)
    return render(request, "mudar_email.html", {"form": form})

@login_required
def confirmar_novo_email(request):
    novo_email = request.session.get("novo_email")

    if not novo_email:
        messages.error(request, "Sessão de confirmação não encontrada.")
        return redirect("mudar_email")

    usuario = request.user

    if request.method == "POST":
        form = CodigoForm(request.POST)
        if form.is_valid():

             # Verifica se o código ainda existe
            if not usuario.codigo_confirmacao:
                messages.error(request, "Não existe um código válido.")

            # Verifica se o código expirou
            elif (timezone.now() >= usuario.codigo_expira_em):
                usuario.codigo_confirmacao = None
                usuario.codigo_expira_em = None
                usuario.save()

                messages.error(request, "Seu código expirou. Solicite um novo.")
                print(request._messages._queued_messages[-1])

            # Verifica o limite de tentativas
            elif usuario.tentativas >= 10:
                messages.error(request, "Você excedeu o limite de tentativas.")
                print(request._messages._queued_messages[-1])
                print("tentativas:", usuario.tentativas)

            else:
                codigo = form.cleaned_data["codigo"]

                if usuario.codigo_confirmacao == codigo:
                    if Usuario.objects.filter(email=novo_email).exclude(pk=usuario.pk).exists():
                        messages.error(request, "Este email já está cadastrado.")
                    else:
                        usuario.email = novo_email
                        usuario.codigo_confirmacao = None
                        usuario.codigo_expira_em = None
                        usuario.tentativas = 0
                        usuario.save()

                        request.session.pop("novo_email", None)

                        messages.success(request, "Código confirmado, email alterado com sucesso.")
                        print(request._messages._queued_messages[-1])

                        return redirect("home")

                else:
                    messages.error(request, "código incorreto")
                    usuario.tentativas += 1
                    usuario.save()
                    print(request._messages._queued_messages[-1])
                    print("tentativas:", usuario.tentativas)
        else:
            messages.error(request, "formulário inválido")
    else:
        form = CodigoForm()
    return render(request, "confirmar_codigo.html", {"form": form})
