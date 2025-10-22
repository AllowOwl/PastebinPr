from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from .decorators import user_required, admin_required, moderator_required

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Вход пользователя - УБЕДИТЕСЬ ЧТО ВСЕ ВЕТКИ ВОЗВРАЩАЮТ HttpResponse"""
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
                return render(request, 'accounts/login.html', {'form': form})
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')

@user_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@admin_required
def admin_panel(request):
    return render(request, 'accounts/admin_panel.html')

@moderator_required
def moderator_panel(request):
    return render(request, 'accounts/moderation_panel.html')