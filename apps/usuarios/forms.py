from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import Usuario


# form de registro baseado no usercreationform do django
class RegistroForm(UserCreationForm):


    class Meta:
        model = Usuario

        # campos exibidos no formulário de cadastro
        fields = [
            "nome",
            "email",
        ]

    # validações
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # dominio_permitido = "ifrn.edu.br"
        # validação para permitir apenas emails institucionais do IFRN
        # if dominio_permitido not in email.split("@")[1]:
            # raise ValidationError("Use um e-mail institucional (domínio: ifrn.edu.br).")

        # Verifica se o e-mail já existe, mas ignora o e-mail do próprio usuário atual
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso por outra conta.")
        return email

# form simples para login
class LoginForm(forms.Form):

    # campo de email (usado como username)
    username = forms.EmailField(label="Email")

    # campo de senha (input oculto)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput())


# form usado pelo admin para editar usuários
class UsuarioAdminForm(UserChangeForm):
    # admin pode alterar tudo, inclusive tipo e status

    class Meta:
        model = Usuario

        fields = [
            "nome",
            "email",
            "is_staff",
            "is_active",
        ]

# Formulário para editar APENAS o nome na pagina editar-usuario


class UsuarioMudarNomeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome"]

# Formulário para editar APENAS o e-mail na pagina editar-email


class UsuarioMudarEmailForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email"]

    # validação de email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se o e-mail já existe, mas ignora o e-mail do próprio usuário atual
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso por outra conta.")
        return email