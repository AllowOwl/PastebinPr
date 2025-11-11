from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pastes/', views.paste_list, name='paste_list'),
    path('pastes/create/', views.create_paste, name='create_paste'),
    path('pastes/<int:paste_id>/', views.paste_detail, name='paste_detail'),
    path('pastes/<int:paste_id>/like/', views.like_paste, name='like_paste'),
    path('pastes/<int:paste_id>/comment/', views.add_comment, name='add_comment'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
]