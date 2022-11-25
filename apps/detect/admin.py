from django.contrib import admin
from .models import InferencedImage, InferencedVideo

# Register your models here.
@admin.register(InferencedImage)
class InferencedImageAdmin(admin.ModelAdmin):
    list_display = ["orig_image", "inf_image_path",
                    "model_conf",]
@admin.register(InferencedVideo)
class InferencedVideoAdmin(admin.ModelAdmin):
    list_display = ["orig_video", "inf_video_path",
                    "model_conf",]