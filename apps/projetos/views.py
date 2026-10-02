from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projeto
from .forms import CriarProjeto

@login_required
def criar_projeto(request):
    if request.method == "POST":
        form = CriarProjeto(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.usuario = request.user
            projeto.save()
            messages.success(request, "Projeto criado com sucesso")
        else:
            messages.error(request, "Falha ao criar projeto")

        return redirect("home")

    else:
        form = CriarProjeto()

        return render(request, "criar_projeto.html", {"form": form, "editar": False})
    

@login_required
def editar_projeto(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    if projeto.usuario == request.user or request.user.is_staff:
        if request.method =="POST":
            form = CriarProjeto(request.POST, instance=projeto)
            if form.is_valid():
                form.save()
                messages.success(request, "Projeto atualizado com sucesso")
            else:
                messages.error(request, "Falha ao atualizar projeto")

            return redirect("home")

        else:
            form = CriarProjeto(instance=projeto)
            return render(request, "criar_projeto.html", {"form": form, "editar": True})
    else:
        messages.error(request, "Você não possuí permissão para executar esta ação")
        return redirect("home")

@login_required
def excluir_projeto(request):
    if request.method == "POST":
        id_projeto = request.POST.get("id")
        projeto = get_object_or_404(Projeto, id=id_projeto)
        if request.user.is_staff or projeto.usuario == request.user:
            projeto.delete()
            messages.success(request, "Projeto excluído com sucesso")
        else:
            messages.error(request, "Você não possui permissão para executar esta ação")

    return redirect("home")
