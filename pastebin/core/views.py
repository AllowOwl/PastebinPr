from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import Q, Count
from django.utils import timezone
from .models import Paste, Topic, Like, Comment
from .forms import PasteForm, CommentForm

def home(request):
    """Главная страница со списком тем и информацией о пользователе"""
    topics = Topic.objects.filter(is_public=True)
    recent_pastes = Paste.get_active_pastes().filter(
        visibility=Paste.Visibility.PUBLIC
    ).select_related('author', 'topic').order_by('-created_at')[:5]

    
    context = {
        'topics': topics,
        'recent_pastes': recent_pastes,
        'user': request.user,
    }
    
    # Используем ваш путь
    return render(request, 'pages/home.html', context)

def topic_detail(request, topic_id):
    """Детали темы со списком паст"""
    topic = get_object_or_404(Topic, id=topic_id, is_public=True)
    pastes = Paste.get_active_pastes().filter(
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
    pastes = Paste.get_active_pastes().filter(
        visibility=Paste.Visibility.PUBLIC
    )

    topic_id = request.GET.get('topic')
    if topic_id:
        pastes = pastes.filter(topic_id=topic_id)

    search_query = request.GET.get('q')
    if search_query:
        pastes = pastes.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'likes':
        pastes = pastes.order_by('-views_count')
    elif sort_by == 'likes':
        pastes = pastes.annotate(like_count=Count('likes')).order_by('-like_count')
    else:
        pastes = pastes.order_by('-created_at')
    
    pastes = pastes.select_related('author', 'topic')

    topics = Topic.objects.filter(is_public=True)

    context = {
        'pastes': pastes,
        'topics': topics,
        'current_topic': topic_id,
        'search_query': search_query or '',
        'sort_by': sort_by,
    }

    return render(request, 'pages/paste_list.html', context)

def paste_detail(request, paste_id):
    """Детали пасты с комментариями"""
    paste = get_object_or_404(Paste.get_active_pastes(), id=paste_id)
    
    # Проверяем права доступа
    if not paste.can_view(request.user):
        raise Http404("Паста не найдена или у вас нет прав для просмотра")
    
    # Увеличиваем счётчик просмотров
    paste.views_count += 1
    paste.save()
    
    # Получаем комментарии
    comments = paste.comments.select_related('author').all()
    
    # Проверяем лайк пользователя
    user_liked = False
    if request.user.is_authenticated:
        user_liked = paste.likes.filter(user=request.user).exists()
    
    context = {
        'paste': paste,
        'comments': comments,
        'user_liked': user_liked,
        'likes_count': paste.likes.count(),
    }
    return render(request, 'pages/paste_detail.html', context)

@login_required
def create_paste(request):
    """Создание новой пасты"""
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            paste = form.save(commit=False)
            paste.author = request.user
            
            # Обработка срока действия
            expires_at = form.cleaned_data.get('expires_at')
            if expires_at:
                paste.expires_at = expires_at
            
            paste.save()
            messages.success(request, 'Паста успешно создана!')
            return redirect('paste_detail', paste_id=paste.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = PasteForm()
    
    # Получаем популярные темы для подсказок
    popular_topics = Topic.objects.filter(
        is_public=True
    ).annotate(
        paste_count=Count('pastes')
    ).order_by('-paste_count')[:10]
    
    context = {
        'form': form,
        'popular_topics': popular_topics,
    }
    return render(request, 'pages/create_paste.html', context)

@login_required
def delete_paste(request, paste_id):
    """Удаление пасты"""
    paste = get_object_or_404(Paste, id=paste_id)
    
    # Сохраняем информацию о теме для обновления
    topic = paste.topic
    
    # Проверяем права на удаление
    if not paste.can_delete(request.user):
        messages.error(request, 'У вас нет прав для удаления этой пасты')
        return redirect('paste_detail', paste_id=paste_id)
    
    if request.method == 'POST':
        paste_title = paste.title
        paste.delete()
        
        # Обновляем время обновления темы, если паста была в теме
        if topic:
            topic.update_updated_at()
        
        messages.success(request, f'Паста "{paste_title}" была успешно удалена')
        return redirect('home')
    
    # Если GET запрос, показываем страницу подтверждения
    context = {
        'paste': paste,
    }
    return render(request, 'pages/confirm_delete.html', context)

@login_required
def like_paste(request, paste_id):
    """Лайк/анлайк пасты"""
    paste = get_object_or_404(Paste, id=paste_id)
    
    if not paste.can_view(request.user):
        raise Http404("Паста не найдена")
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        paste=paste
    )
    
    if not created:
        like.delete()
        messages.info(request, 'Лайк удален')
    else:
        messages.success(request, 'Паста понравилась!')
    
    return redirect('paste_detail', paste_id=paste_id)

@login_required
def add_comment(request, paste_id):
    """Добавление комментария к пасте"""
    paste = get_object_or_404(Paste, id=paste_id)
    
    if not paste.can_view(request.user):
        raise Http404("Паста не найдена")
    
    if not paste.can_delete(request.user):
        messages.error(request, 'У вас нет прав для удаления этой пасты')
        return redirect('paste_detail', paste_id=paste_id)
    
    if request.method == 'POST':
        paste_title = paste.title
        paste.delete()
        messages.success(request, f'Паста "{paste_title}" была успешно удалена')
        return redirect('home')
    
    # Если GET запрос, показываем страницу подтверждения
    context = {
        'paste': paste,
    }
    return render(request, 'pages/confirm_delete.html', context)