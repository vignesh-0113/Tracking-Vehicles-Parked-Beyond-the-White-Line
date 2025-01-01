import os
import json
import cv2
import pytesseract
from datetime import datetime
from django.shortcuts import render
from .forms import VideoUploadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# Set the path to Tesseract OCR (update this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust if needed

def process_video(video_path):
    vehicle_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')
    cap = cv2.VideoCapture(video_path)
    vehicle_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vehicles = vehicle_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in vehicles:
            vehicle_plate_region = frame[y:y + h, x:x + w]
            plate_text = pytesseract.image_to_string(vehicle_plate_region, config='--psm 8')
            plate_text = plate_text.strip()

            detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if plate_text:
                vehicle_data.append({
                    'vehicle_number': plate_text,
                    'license': 'UNKNOWN',  # You can enhance this with a license API if needed
                    'detection_time': detection_time
                })

    cap.release()

    # Save data to a JSON file
    json_file_path = os.path.join(settings.MEDIA_ROOT, 'vehicle_data.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(vehicle_data, json_file, indent=4)

    return json_file_path

def video_upload_view(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        uploaded_file_url = fs.url(filename)

        # Process the video
        video_path = os.path.join(settings.MEDIA_ROOT, filename)
        json_file_path = process_video(video_path)

        return render(request, 'dashboard/video_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'json_file_url': json_file_path
        })

    form = VideoUploadForm()
    return render(request, 'dashboard/video_upload.html', {'form': form})

def vehicle_list(request):
    # Load the vehicle data from the JSON file
    json_file_path = os.path.join(settings.MEDIA_ROOT, 'vehicle_data.json')
    
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            vehicle_data = json.load(json_file)
    else:
        vehicle_data = []

    return JsonResponse({'vehicle': vehicle_data})
