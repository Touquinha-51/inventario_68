from django.shortcuts import render

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
