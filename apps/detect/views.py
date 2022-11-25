import os
import io
from PIL import Image as I
import torch
import collections
from ast import literal_eval
import cv2
import numpy as np

from django.views.generic.detail import DetailView
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator

from apps.images.models import ImageFile
from apps.videos.models import VideoFile
from .models import InferencedImage, InferencedVideo
from .forms import InferencedImageForm, YoloModelForm

class InferencedImageDetectionView(DetailView):
    model = ImageFile
    template_name = "detectobj/select_inference_image.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img_qs = self.get_object()
        imgset = img_qs.image_set

        is_inf_img = InferencedImage.objects.filter(
            orig_image=img_qs).exists()
        if is_inf_img:
            inf_img_qs = InferencedImage.objects.get(orig_image=img_qs)
            context['inf_img_qs'] = inf_img_qs

        context["img_qs"] = img_qs
        context["form1"] = YoloModelForm()
        context["form2"] = InferencedImageForm()
        return context

    def post(self, request, *args, **kwargs):
        img_qs = self.get_object()
        img_bytes = img_qs.image.read()
        img = I.open(io.BytesIO(img_bytes))

        # Get form data
        modelconf = self.request.POST.get("confidence")
        if modelconf:
            modelconf = float(modelconf)
        else:
            modelconf = settings.MODEL_CONFIDENCE
        # custom_model_id = self.request.POST.get("custom_model")
        yolo_model_name = self.request.POST.get("yolo_model")

        # Yolov5 dirs
        yolo_dir = settings.YOLOV5_ROOTDIR
        yolo_weightsdir = settings.YOLOV5_WEIGTHS_DIR

        
        if yolo_model_name:
            model = torch.hub.load(
                yolo_dir,  # path to hubconf file
                'custom',
                # Yolov5 model path yolov5/weights/<model_name>.pt
                path=os.path.join(yolo_weightsdir, yolo_model_name),
                source='local',
                force_reload=True,
            )

        model.conf = modelconf

        results = model(img, size=640)
        results_list = results.pandas().xyxy[0].to_json(orient="records")
        results_list = literal_eval(results_list)
        classes_list = [item["name"] for item in results_list]
        results_counter = collections.Counter(classes_list)
        if results_list == []:
            messages.warning(
                request, f'Model "{detection_model.name}" unable to predict. Try with another model.')
        else:
            results.render()
            media_folder = settings.MEDIA_ROOT
            inferenced_img_dir = os.path.join(
                media_folder, "inferenced_image")
            if not os.path.exists(inferenced_img_dir):
                os.makedirs(inferenced_img_dir)
            for img in results.ims:
                img_base64 = I.fromarray(img)
                img_base64.save(
                    f"{inferenced_img_dir}/{img_qs}", format="JPEG")

            # Create/update the inferencedImage instance
            inf_img_qs, created = InferencedImage.objects.get_or_create(
                orig_image=img_qs,
                inf_image_path=f"{settings.MEDIA_URL}inferenced_image/{img_qs.name}",
            )
            inf_img_qs.detection_info = results_list
            inf_img_qs.model_conf = modelconf
            # if custom_model_id:
            #     inf_img_qs.custom_model = detection_model
            if yolo_model_name:
                inf_img_qs.yolo_model = yolo_model_name
            inf_img_qs.save()
        torch.cuda.empty_cache()

        # set image is_inferenced to true
        img_qs.is_inferenced = True
        img_qs.save()
        # Ready for rendering next image on same html page.
        imgset = img_qs.image_set
        images_qs = imgset.images.all()

        context = {}
        context["img_qs"] = img_qs
        context["images_qs"] = images_qs
        context["inferenced_img_dir"] = f"{settings.MEDIA_URL}inferenced_image/{img_qs}"
        context["results_list"] = results_list
        context["results_counter"] = results_counter
        context["form1"] = YoloModelForm()
        context["form2"] = InferencedImageForm()
        return render(self.request, self.template_name, context)

class InferencedVideoDetectionView(DetailView):
    model = VideoFile
    template_name = "detectobj/select_inference_video.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_qs = self.get_object()
        videoset = video_qs.video_set

        is_inf_video = InferencedVideo.objects.filter(
            orig_video=video_qs).exists()
        if is_inf_video:
            is_inf_video = InferencedVideo.objects.get(orig_video=video_qs)
            context['inf_video_qs'] = is_inf_video

        context["video_qs"] = video_qs
        context["form1"] = YoloModelForm()
        context["form2"] = InferencedImageForm()
        return context

    def post(self, request, *args, **kwargs):
        video_qs = self.get_object()
        # print(video_qs.get_videourl)
        cap = cv2.VideoCapture(f'D:\\Workspace\\ProjectDjango\\btl\\media\\None\\videos\\{video_qs}')

        yolo_dir = settings.YOLOV5_ROOTDIR
        yolo_weightsdir = settings.YOLOV5_WEIGTHS_DIR
        model = torch.hub.load(
                    yolo_dir,  # path to hubconf file
                    'custom',
                    # Yolov5 model path yolov5/weights/<model_name>.pt
                    path=os.path.join(yolo_weightsdir, 'best'),
                    source='local',
                    force_reload=True,
                )

        if (cap.isOpened()== False): 
            print("Error opening video stream or file")
 
        # Read until video is completed
        while(cap.isOpened()):
        # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:

                results = model(frame, augment=True)
                results.render()

                # for i in results.render():
                #     print(i)
        #             cv2image = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        #             data = I.fromarray(cv2image)
        #             data.save('demo.jpg')
        #         cv2.imwrite('demo.jpg', frame)

        #         # Display the resulting frame
        #         yield (b'--frame\r\n'
        #                 b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')
                cv2.imshow('Frame',frame)
            
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                # return HttpResponse('Ok')
        # Break the loop
            else: 
                break
        # # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()