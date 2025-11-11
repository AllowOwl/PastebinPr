from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название темы")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True, verbose_name="Публичная тема")

    class Meta:
        ordering = ['title']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'topic_id': self.id})
    
    def public_pastes_count(self):
        return self.pastes.filter(visibility=Paste.Visibility.PUBLIC).count()
        
class Paste(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Публичная'
        PRIVATE = 'private', 'Приватная'
        UNLISTED = 'unlisted', 'Скрытая'
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pastes',
        verbose_name="Автор"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pastes',
        verbose_name="Тема"
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        verbose_name="Видимость"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Истекает")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Паста"
        verbose_name_plural = "Пасты"
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['author', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('paste_detail', kwargs={'paste_id': self.id})
    
    def is_public(self):
        return self.visibility == self.Visibility.PUBLIC
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def can_view(self, user):
        if self.is_expired():
            return False
        if self.visibility == self.Visibility.PUBLIC:
            return True
        if user.is_authenticated:
            if self.visibility == self.Visibility.UNLISTED:
                return True
            if self.author == user:
                return True
        return False
    
    def get_display_content(self):
        if len(self.content) > 500:
            return self.content[:500] + "..."
        return self.content
    
class Comment(models.Model):
    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Паста"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commetns',
        verbose_name="Автор",
    )
    content = models.TextField(verbose_name="Содержание комментария")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Комментарий"
        verbose_name_plural = "Коментарии"
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.paste.title}"
    
    def get_absolute_url(self):
        return reverse('paste_detail', kwargs={'paste_id': self.paste.id}) + f'#comment-{self.id}'
    
class Like(models.Model):
    """Модель для лайков паст"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Пользователь"
    )
    paste = models.ForeignKey(
        Paste,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Паста"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'paste']  # Один пользователь может лайкнуть пасту только один раз
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.paste.title}"