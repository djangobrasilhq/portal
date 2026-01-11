from django import forms
from accounts.models import User

class UserProfileForm(forms.ModelForm):
    """Formulário para o perfil do usuário"""
    class Meta:
        model = User
        fields = ["gitlab", "gitbucket", "linkedin", "twitter", "website", "bio"]
        widgets = {
            "gitlab": forms.TextInput(attrs={
                "placeholder": "https://gitlab.com/seu-usuario",
                "class": "form-input"
            }),
            "gitbucket": forms.TextInput(attrs={
                "placeholder": "https://bitbucket.org/seu-usuario",
                "class": "form-input"
            }),
            "linkedin": forms.TextInput(attrs={
                "placeholder": "https://linkedin.com/in/seu-perfil",
                "class": "form-input"
            }),
            "twitter": forms.TextInput(attrs={
                "placeholder": "@seu-usuario",
                "class": "form-input"
            }),
            "website": forms.URLInput(attrs={
                "placeholder": "https://seusite.com",
                "class": "form-input"
            }),
            "bio": forms.Textarea(attrs={
                "placeholder": "Conte um pouco sobre você...",
                "class": "form-input",
                "rows": 4
            }),
        }