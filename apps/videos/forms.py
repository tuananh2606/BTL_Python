from django import forms
from .models import VideoFile

class VideosFileForm(forms.Form):
    class Meta:
        model = VideoFile
        fields = ['name','video']