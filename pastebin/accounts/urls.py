from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('moderation/', views.moderator_panel, name='moderator_panel'),
]