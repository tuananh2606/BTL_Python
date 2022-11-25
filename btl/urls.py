"""btl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.images.views import HomeTemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('students.urls'), name="home_url"),
    path('test/', HomeTemplateView.as_view(), name="test_url"),
    path('', include('apps.images.urls')),
    path('', include('apps.detect.urls')),
    path('', include('apps.webcam.urls')),
    path('', include('apps.videos.urls')),
    path('', include('apps.user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)