from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('create_video_set/', views.VideoSetCreateView.as_view(),
         name='videoset_create_url'),

    path('<int:pk>/update_video_set/', views.VideoSetUpdateView.as_view(),
         name='videoset_update_url'),

    path('video_set_list/', views.VideoSetListView.as_view(),
         name='videoset_list_url'),

    path('<int:pk>/videoset/', views.VideoSetDetailView.as_view(),
         name='videoset_detail_url'),

    path('<int:pk>/upload_videos/', views.VideosUploadView.as_view(),
         name='upload_videos_url'),

    path('<int:pk>/videos_list/', views.VideosListView.as_view(),
         name='videos_list_url'),

    path('<int:imgset_pk>/delete_video/<int:pk>/', views.VideosDeleteUrl.as_view(),
         name='video_delete_url'),

     path('delete_videoset/<int:pk>/', views.VideosetDeleteUrl.as_view(),
         name='videoset_delete_url'),
]
