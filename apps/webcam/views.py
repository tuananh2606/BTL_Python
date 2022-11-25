from django.shortcuts import render
from .models import *
from PIL import Image as im
from django.conf import settings
from django.http import StreamingHttpResponse
import cv2
import torch
import os

# def infer(img):
#     height, width = img.shape[:2]
#     scale = 640 / max(height, width)
#     img = cv2.resize(img, (round(scale * width), round(scale * height)))

def stream():
    cap = cv2.VideoCapture(0)
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
    while True:
        ret, frame = cap.read()
        # frame = infer(frame)
        if not ret:
            print("Error: failed to capture image")
            break
        
        height, width = frame.shape[:2]
        scale = 640 / max(height, width)
        frame = cv2.resize(frame, (round(scale * width), round(scale * height)))

        results = model(frame, augment=True)
        
        for i in results.render():
            cv2image = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
            data = im.fromarray(cv2image)
            data.save('demo.jpg')
        cv2.imwrite('demo.jpg', frame)
        # proccess    
        # image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

        if cv2.waitKey(1) == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')