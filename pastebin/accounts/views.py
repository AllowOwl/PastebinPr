from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, UserEditForm
from .decorators import user_required, admin_required, moderator_required
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')

@user_required
def profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'form': form
    })

@admin_required
def admin_panel(request):
    # Получаем всех пользователей кроме текущего админа
    users = CustomUser.objects.exclude(id=request.user.id).order_by('-date_joined')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(CustomUser, id=user_id)
        
        if action == 'make_moderator':
            user.role = CustomUser.Role.MODDERATOR
            user.save()
            messages.success(request, f'Пользователь {user.username} теперь модератор!')
        elif action == 'make_user':
            user.role = CustomUser.Role.USER
            user.save()
            messages.success(request, f'Пользователь {user.username} теперь обычный пользователь!')
        elif action == 'make_admin':
            user.role = CustomUser.Role.ADMIN
            user.save()
            messages.success(request, f'Пользователь {user.username} теперь администратор!')
        elif action == 'delete_user':
            if user != request.user:  # Не позволяем удалить себя
                username = user.username
                user.delete()
                messages.success(request, f'Пользователь {username} удален!')
            else:
                messages.error(request, 'Вы не можете удалить свой собственный аккаунт!')
        
        return redirect('admin_panel')
    
    return render(request, 'accounts/admin_panel.html', {
        'users': users,
        'current_user': request.user
    })

@moderator_required
def moderator_panel(request):
    # Здесь можно добавить функционал для модераторов
    # Например, модерация паст, комментариев и т.д.
    return render(request, 'accounts/moderation_panel.html', {
        'user': request.user
    })