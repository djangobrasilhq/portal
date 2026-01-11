from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import UserProfileForm


def login_redirect(request):
    """Redireciona automaticamente para o login social do GitHub"""
    return redirect("social:begin", "github")


@login_required
def logout_view(request):
    """Faz logout do usuário e redireciona para home"""
    logout(request)
    return redirect("home")


@login_required
def user_profile(request):
    """Exibe o perfil do usuário"""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações salvas com sucesso.")
            return redirect("user_profile")
        else:
            messages.error(request, "Erro ao salvar o formulário. Verifique os campos.")
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, "accounts/profile.html", {"user": request.user, "form": form})
    