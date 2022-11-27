import os
from PIL import Image as I

from django.db import models
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ImageSet(models.Model):
    name = models.CharField(max_length=100,
                            help_text="eg. flowers"
                            )
    description = models.TextField()
    dirpath = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name'],
            name='unique_imageset_by_user')]

    def __str__(self):
        return f'{self.name.capitalize()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("save() called")
    save.alters_data = True

    def get_delete_url(self):
        return reverse("images:imageset_list_url", kwargs={})

    # def get_dirpath(self):
    #     rootdir = os.path.join(self.user.username, self.name)
    #     return rootdir

    def get_absolute_url(self):
        return reverse("images:imageset_detail_url", kwargs={"pk": self.pk})


def imageset_upload_images_path(instance, filename):
    return f'{instance.image_set.dirpath}/images/{filename}'

class ImageFile(models.Model):
    name = models.CharField(_('Image Name'), max_length=150, null=True)
    image_set = models.ForeignKey('images.ImageSet',
                                  related_name="images",
                                  on_delete=models.CASCADE,
                                  help_text="Image Set of the uploading images"
                                  )
    image = models.ImageField(upload_to=imageset_upload_images_path)

    is_inferenced = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @ property
    def get_imageurl(self):
        return self.image.url

    @ property
    def get_imagepath(self):
        return self.image.path

    @ property
    def get_filename(self):
        return os.path.split(self.image.url[-1])

    @ property
    def get_imgshape(self):
        im = I.open(self.get_imagepath)
        return im.size

    def get_delete_url(self):
        return reverse("images:images_list_url", kwargs={"pk": self.image_set.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = I.open(self.get_imagepath)
        if img.height >= 640 and img.width >= 640:
            output_size = (640, 640)
            img.thumbnail(output_size)
            img.save(self.get_imagepath)
        else:
            print("ảnh lỗi rồi bạn ơi")

