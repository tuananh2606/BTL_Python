import random
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from PIL import Image as im
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.views.generic import View
from django.shortcuts import get_object_or_404, render

from .models import ImageFile, ImageSet

# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = "images/mainview.html"

class ImageSetCreateView(CreateView):
    model = ImageSet
    fields = ['name', 'description']

    def form_valid(self, form):
        if not ImageSet.objects.filter(name=form.instance.name).exists():
            return super().form_valid(form)
        else:
            form.add_error(
                'name',
                f"Imageset with name {form.cleaned_data['name']} already exists in dataset. \
                     Add more images to that imageset, if required."
            )
            return HttpResponseRedirect(reverse('images:imageset_create_url'))


class ImageSetUpdateView(UpdateView):
    model = ImageSet
    fields = ['name', 'description']

    def form_valid(self, form):
        if not ImageSet.objects.filter(name=form.instance.name).exists():
            return super().form_valid(form)
        else:
            print("entered in else")
            form.add_error(
                'name',
                f"Imageset with name {form.cleaned_data['name']} already exists in dataset. \
                     Add more images to that imageset, if required."
            )
            context = {
                'form': form
            }
            return render(self.request, 'images/imageset_form.html', context)

    def get_success_url(self):
        return reverse('images:imageset_detail_url', kwargs={'pk': self.object.id})


class ImageSetListView(ListView):
    model = ImageSet
    context_object_name = 'imagesets'

    # def get_queryset(self):
    #     return super().get_queryset()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["user_imagesets"] = ImageSet.objects.all()
    #     print(context)
    #     return context


class ImageSetDetailView(DetailView):
    model = ImageSet
    context_object_name = 'imageset'


class ImagesUploadView(View):
    def get(self, request, *args, **kwargs):
        imageset_id = self.kwargs.get("pk")
        imageset = get_object_or_404(ImageSet, id=imageset_id)
        context = {
            'imageset': imageset,
        }
        return render(request, 'images/imagefile_form.html', context)

    def post(self, request, *args, **kwargs):
        imageset_id = self.kwargs.get("pk")
        imageset = get_object_or_404(ImageSet, id=imageset_id)
        if self.request.method == 'POST':
            images = [self.request.FILES.get("file[%d]" % i)
                      for i in range(0, len(self.request.FILES))]
                        
            for f in request.FILES.getlist('file'):
                image = ImageFile(name=f.name, image=f, image_set=imageset)
                image.save()

            # for img in images:
                
            #     if not ImageFile.objects.filter(name=img.name, image_set=imageset).exists():
            #         ImageFile.objects.create(
            #             name=img.name, image=img, image_set=imageset)

            #     else:
            #         print(f"Image {img.name} already exists in the imageset.")

            message = f"Uploading images to the Imageset: {imageset}. \
                Automatic redirect to the images list after completion."

            redirect_to = reverse_lazy(
                "images:images_list_url", args=[imageset.id])
            return JsonResponse({"result": "result",
                                "message": message,
                                 "redirect_to": redirect_to,
                                 "files_length": len(images),
                                 },
                                status=200,
                                content_type="application/json"
                                )


class ImagesListView(ListView):
    model = ImageFile
    context_object_name = 'images'

    def get_queryset(self):
        imageset_id = self.kwargs.get('pk')
        return super().get_queryset().filter(image_set__id=imageset_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imageset_id = self.kwargs.get('pk')
        imageset = get_object_or_404(ImageSet, id=imageset_id)
        context["imageset"] = imageset
        return context


class ImagesDeleteUrl(DeleteView):
    model = ImageFile

    def get_success_url(self):
        qs = self.get_object()
        return qs.get_delete_url()

class ImagesetDeleteUrl(DeleteView):
    model = ImageSet

    def get_success_url(self):
        qs = self.get_object()
        print(qs)
        return qs.get_delete_url()