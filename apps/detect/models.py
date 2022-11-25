from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class InferencedImage(models.Model):
    orig_image = models.ForeignKey(
        "images.ImageFile",
        on_delete=models.CASCADE,
        related_name="detectedimages",
        help_text="Main Image",
        null=True,
        blank=True
    )

    inf_image_path = models.CharField(max_length=250,
                                      null=True,
                                      blank=True
                                      )

    # detection_info = models.JSONField(null=True, blank=True)

    YOLOMODEL_CHOICES = [
        ('yolov5s.pt', 'yolov5s.pt'),
        ('yolov5m.pt', 'yolov5m.pt'),
        ('yolov5l.pt', 'yolov5l.pt'),
        ('yolov5x.pt', 'yolov5x.pt'),
        ('best.pt', 'best.pt'),
    ]

    yolo_model = models.CharField(_('YOLOV5 Models'),
                                  max_length=250,
                                  null=True,
                                  blank=True,
                                  choices=YOLOMODEL_CHOICES,
                                  default=YOLOMODEL_CHOICES[0],
                                  help_text="Selected yolo model will download. \
                                 Requires an active internet connection."
                                  )

    model_conf = models.DecimalField(_('Model confidence'),
                                     decimal_places=2,
                                     max_digits=4,
                                     null=True,
                                     blank=True)

class InferencedVideo(models.Model):
    orig_video = models.ForeignKey(
        "videos.VideoFile",
        on_delete=models.CASCADE,
        related_name="detectedvideos",
        help_text="Main Video",
        null=True,
        blank=True
    )

    inf_video_path = models.CharField(max_length=250,
                                      null=True,
                                      blank=True
                                      )

    YOLOMODEL_CHOICES = [
        ('yolov5s.pt', 'yolov5s.pt'),
        ('yolov5m.pt', 'yolov5m.pt'),
        ('yolov5l.pt', 'yolov5l.pt'),
        ('yolov5x.pt', 'yolov5x.pt'),
        ('best.pt', 'best.pt'),
    ]

    yolo_model = models.CharField(_('YOLOV5 Models'),
                                  max_length=250,
                                  null=True,
                                  blank=True,
                                  choices=YOLOMODEL_CHOICES,
                                  default=YOLOMODEL_CHOICES[0],
                                  help_text="Selected yolo model will download. \
                                 Requires an active internet connection."
                                  )

    model_conf = models.DecimalField(_('Model confidence'),
                                     decimal_places=2,
                                     max_digits=4,
                                     null=True,
                                     blank=True)