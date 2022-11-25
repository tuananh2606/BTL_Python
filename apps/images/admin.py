from django.contrib import admin
from .models import ImageSet, ImageFile

# Register your models here.
@admin.register(ImageSet)
class ImageSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_set', 'image', 'is_inferenced']