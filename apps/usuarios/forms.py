from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Usuario


# form de registro baseado no usercreationform do django
class RegistroForm(UserCreationForm):


    class Meta:
        model = Usuario

        # campos exibidos no formulário de cadastro
        fields = [
            "nome",
            "email",
            "senha",
            "senha_confirmacao",
        ]

    nome = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nome de usuário"}),
    )

    # campo email obrigatório com input customizado
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"}),
    )

    # personalização dinâmica dos campos de senha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["senha"].widget.attrs.update(
            {"placeholder": "Senha"}
        )

        self.fields["senha_confirmacao"].widget.attrs.update(
            {"placeholder": "Confirme a senha"}
        )

    # validações
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já foi cadastrado por algum usuário.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get("senha")
        nome = self.instance  # Opcional: ajuda o validador de similaridade

        if senha1:
            try:
                # Valida contra as regras do settings.py
                validate_password(senha1, nome)
            except ValidationError as e:
                # Adiciona o erro especificamente ao campo de senha
                self.add_error('senha', e)

        return cleaned_data


# form simples para login
class LoginForm(forms.Form):

    # campo de usuário
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"}),
    )

    # campo de senha (input oculto)
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Senha"}),
    )


# form usado pelo admin para editar usuários
class UsuarioAdminForm(forms.ModelForm):
    # admin pode alterar tudo, inclusive tipo e status

    class Meta:
        model = Usuario

        fields = [
            "nome",
            "email",
            "tipo",
            "is_active",
        ]

        # customização visual dos campos
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome"}),
            "email": forms.EmailInput(attrs={"placeholder": "E-mail"}),
            "tipo": forms.Select(attrs={}),
            "is_active": forms.CheckboxInput(attrs={}),
        }

# Formulário para editar APENAS o nome na pagina editar-usuario


class UsuarioUpdateNomeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Novo nome"}),
        }

# Formulário para editar APENAS o e-mail na pagina editar-email


class UsuarioUpdateEmailForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Novo e-mail"}),
        }

    # Reutiliza a validação de email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se o e-mail já existe, mas ignora o e-mail do próprio usuário atual
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso por outra conta.")
        return email


class UsuarioUpdateTipoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['tipo']