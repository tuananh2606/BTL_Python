from django.urls import path
from . import views

app_name = 'webcam'

urlpatterns = [
    path('stream/', views.video_feed, name='stream'),
]
