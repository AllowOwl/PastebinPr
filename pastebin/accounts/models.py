from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'  # Исправлено с MODDERATOR на MODERATOR

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.USER,
    )

    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_user(self):
        return self.role == self.Role.USER 
    
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def is_moderator(self):
        return self.role == self.Role.MODERATOR