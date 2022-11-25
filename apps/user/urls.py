from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.index_login,
         name='index_login'),
    path('video_login/', views.video_login,
         name='video_login'),
    path('handle_login/', views.handle_login,
         name='handle_login'),
    path('register/', views.register_new_user,
         name='register'),
         
]