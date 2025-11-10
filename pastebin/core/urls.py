from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pastes/', views.paste_list, name='paste_list'),
    path('pastes/<int:paste_id>/', views.paste_detail, name='paste_detail'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
]