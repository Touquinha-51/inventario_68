from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistroForm, UsuarioAdminForm
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    add_form = RegistroForm
    form = UsuarioAdminForm
    model = Usuario

    list_display = ["email", "nome", "is_staff", "is_active", "is_superuser", "criado_em"]

    # Ordenação padrão da tabela
    ordering = ["criado_em"]

    # Como os campos aparecem na tela de EDIÇÃO de usuário
    fieldsets = (
        ("Informações do Usuário", {"fields": ("email", "nome", "password"), }),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    # Como os campos aparecem na tela de CRIAÇÃO de usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("nome", "email", "password1", "password2"),
        }),
    )