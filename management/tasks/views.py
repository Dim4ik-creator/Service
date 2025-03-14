from idlelib.rpc import request_queue
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, "main/index.html")


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Проверка совпадения паролей
        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'main/register.html')

        # Проверка наличия пользователя с таким логином или почтой
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'main/register.html')

        # if CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, 'Пользователь с таким адресом электронной почты уже существует.')
        #     return render(request, 'main/register.html')

        # Создание и сохранение пользователя
        user = CustomUser.objects.create_user(username=username, password=password)
        user.name = full_name  # Django сохраняет только отдельные поля first_name и last_name
        user.save()
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Аутентификация после регистрации
            return redirect('home')

        return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                messages.error(request, "Вы не можете войти здесь как администратор.")
            else:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'admin_dashboard.html')

@login_required
def tasks(request):
    return render(request,"main/tasks.html")
