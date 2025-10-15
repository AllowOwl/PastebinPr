from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home page'),
    path('pastes/', views.paste_list, name='paste_list'),
    path('pastes/<int:paste_id>/', views.paste_detail, name='paste_detail'),
]