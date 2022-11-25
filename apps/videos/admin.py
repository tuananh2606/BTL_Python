from django.contrib import admin
from .models import VideoSet, VideoFile

# Register your models here.
@admin.register(VideoSet)
class VideoSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'video_set', 'video', 'is_inferenced']