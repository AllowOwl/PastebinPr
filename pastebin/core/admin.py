from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Topic, Paste

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'topic', 'visibility', 'created_at']
    list_filter = ['topic', 'visibility', 'created_at']
    search_fields = ['title', 'content', 'author__username']