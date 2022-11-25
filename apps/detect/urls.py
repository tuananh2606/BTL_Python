from django.urls import path
from . import views

app_name = "detect"

urlpatterns = [
    path("<int:pk>/selected_image/",
         views.InferencedImageDetectionView.as_view(),
         name="detection_image_detail_url"
         ),
    path("<int:pk>/selected_video/",
         views.InferencedVideoDetectionView.as_view(),
         name="detection_video_detail_url"
         ),
]