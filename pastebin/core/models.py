from django.db import models
from django.conf import settings
from django.urls import reverse

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
    syntax = models.CharField(max_length=50, default='text', verbose_name="Синтаксис")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_cout = models.IntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Паста"
        verbose_name_plural = "Пасты"
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('paste_detail', kwargs={'paste_id': self.id})
    
    def is_public(self):
        return self.visibility == self.Visibility.PUBLIC

    