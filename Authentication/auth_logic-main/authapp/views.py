from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
from .forms import LoginForm, RegisterForm 
from .encriptacion import validatePassword, cryptPassword
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            try:
                user = User.objects.get(email=email)
                if validatePassword(password, user.password):
                    login(request, user)  
                    return redirect("dashboard")  
                else:
                    return render(request, "error.html", {"error": "Contraseña incorrecta"})
            except User.DoesNotExist:
                return render(request, "error.html", {"error": "Usuario no encontrado"})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})  


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data.get("role", "user")
            
            encrypted_password = cryptPassword(password)  
            User.objects.create(email=email, password=encrypted_password, role=role)

            return redirect("login")  
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html") 

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')