from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Task
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import JsonResponse


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

        # Проверка наличия пользователя с таким логином
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'main/register.html')

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


@csrf_protect
@login_required
def board_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')

        if title and description and status:
            Task.objects.create(
                title=title,
                description=description,
                status=status,
                creator=request.user
            )

            return redirect('board')

    tasks = Task.objects.filter(creator=request.user)
    users = CustomUser.objects.all()
    from .forms import TaskForm
    form = TaskForm()
    return render(request, 'main/tasks.html', {
        'tasks': tasks,
        'users': users,
        'form': form,
    })


@csrf_protect
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.save()
        return redirect('board')


@csrf_protect
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('board')


@csrf_exempt
@login_required
def update_status(request, task_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            task = Task.objects.get(pk=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})
