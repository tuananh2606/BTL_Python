from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
import os.path
from tkinter import *
import subprocess
from .forms import NameForm
import cv2
from students.models import Student
from pathlib import Path

def index_login(request):
    return render (request, "user/login.html")


def add_webcam():
    global frame
    key = cv2. waitKey(1)
    cap = cv2.VideoCapture(0)
    
    while True:
        try:
            check, frame = cap.read()
            image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
    
        except(KeyboardInterrupt):
            print("Turning off camera.")
            cap.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
       

def video_login(request):
    return StreamingHttpResponse(add_webcam(), content_type='multipart/x-mixed-replace; boundary=frame')   

students = Student.objects.all()
print(students)

path_parent = Path(f'{students[0]}')

db_dir = path_parent.parent.absolute()
unknown_img_path = './.tmp.jpg'
path = f'{db_dir}\./.tmp.jpg'

db = f'{db_dir}'


def handle_login(request):
    cv2.imwrite(unknown_img_path,frame)
    output = str(subprocess.check_output(['face_recognition', db, unknown_img_path]))
    name = output.split(',')[1][:-5]
    print(output)
    print(name)
    


    if name in ['unknown_person', 'no_persons_found']:
        os.remove(unknown_img_path)
        return render(request, "user/message.html")
    else:
        os.remove(unknown_img_path)
        return HttpResponseRedirect("/")

    

def register_new_user(request):

    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form['name'].value()
            path1 = f'{db_dir}\{name}.jpg'
            cv2.imwrite(path1,frame)
            student = Student(first_name=name, image=path1)
            student.save()
               
            
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/login')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'user/register.html', {'form': form})