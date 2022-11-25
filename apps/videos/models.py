import os
from PIL import Image as I

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class VideoSet(models.Model):
    name = models.CharField(max_length=100,
                            help_text="eg. flowers"
                            )
    description = models.TextField()
    dirpath = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name'],
            name='unique_videoset_by_user')]

    def __str__(self):
        return f'{self.name.capitalize()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("save() called")
    save.alters_data = True

    def get_absolute_url(self):
        return reverse("videos:videoset_detail_url", kwargs={"pk": self.pk})


def videoset_upload_videos_path(instance, filename):
    return f'{instance.video_set.dirpath}/videos/{filename}'

class VideoFile(models.Model):
    name = models.CharField(_('Video Name'), max_length=150, null=True)
    video_set = models.ForeignKey('videos.VideoSet',
                                  related_name="videos",
                                  on_delete=models.CASCADE,
                                  help_text="Video Set of the uploading videos"
                                  )
    video = models.FileField(upload_to=videoset_upload_videos_path)

    is_inferenced = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @ property
    def get_videourl(self):
        return self.video.url

    @ property
    def get_videopath(self):
        return self.video.path

    @ property
    def get_filename(self):
        return os.path.split(self.video.url[-1])

    @ property
    def get_imgshape(self):
        im = I.open(self.get_videopath)
        return im.size

    def get_delete_url(self):
        return reverse("videos:videos_list_url", kwargs={"pk": self.video_set.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)