from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    remember_user = request.POST.get("remember")
                    if not remember_user:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(60 * 60 * 24)
                    return redirect("credits:home")
                else:
                    form.add_error(None, "Account is disabled")
            else:
                form.add_error(None, "Incorrect email or password")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            return render(
                request, "accounts/register_done.html", {"new_user": new_user}
            )
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("accounts:login")
