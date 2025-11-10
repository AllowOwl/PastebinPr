from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import Q, Count
from .models import Paste, Topic, Like, Comment

def home(request):
    """Главная страница со списком тем и информацией о пользователе"""
    topics = Topic.objects.filter(is_public=True)
    recent_pastes = Paste.objects.filter(
        visibility=Paste.Visibility.PUBLIC
    ).select_related('author', 'topic')[:5]
    
    context = {
        'topics': topics,
        'recent_pastes': recent_pastes,
        'user': request.user,
    }
    
    # Используем ваш путь
    return render(request, 'pages/home.html', context)

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, is_public=True)
    pastes = Paste.objects.filter(
        topic=topic,
        visibility=Paste.Visibility.PUBLIC
    ).select_related('author').order_by('-created_at')
    
    context = {
        'topic': topic,
        'pastes': pastes,
        'user': request.user,
    }
    return render(request, 'pages/topic_detail.html', context)

def paste_list(request):
    pastes = Paste.objects.filter(
        visibility=Paste.Visibility.PUBLIC
    ).select_related('author', 'topic')
    
    context = {
        'pastes': pastes,
    }
    # Создаем этот файл или используем существующий
    return render(request, 'pages/paste_list.html', context)

def paste_detail(request, paste_id):
    paste = Paste.objects.get(id=paste_id)
    
    # Увеличиваем счётчик просмотров
    paste.views_count += 1
    paste.save()
    
    context = {
        'paste': paste,
    }
    # Создаем этот файл или используем существующий
    return render(request, 'pages/paste_detail.html', context)