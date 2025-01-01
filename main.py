import cv2
import pytesseract
import json
from datetime import datetime
import os

# Set path to tesseract (this is needed if not set globally)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to detect vehicle number plate and save details
def extract_vehicle_details(video_path):
    # Ensure the path to the cascade is correct
    vehicle_cascade_path = cv2.data.haarcascades + 'haarcascade_car.xml'
    
    if not os.path.exists(vehicle_cascade_path):
        print(f"Error: {vehicle_cascade_path} does not exist.")
        return

    # Load the pre-trained vehicle classifier
    vehicle_cascade = cv2.CascadeClassifier(vehicle_cascade_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    vehicle_data = []  # Store detected vehicle details

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect vehicles
        vehicles = vehicle_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in vehicles:
            # Draw a rectangle around the detected vehicle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Crop the number plate region from the image
            vehicle_plate_region = frame[y:y + h, x:x + w]
            plate_text = pytesseract.image_to_string(vehicle_plate_region, config='--psm 8')
            
            # Clean up the number plate text
            plate_text = plate_text.strip()

            # Capture the date-time of detection
            detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Save the details to the list
            if plate_text:
                vehicle_data.append({
                    'vehicle_number': plate_text,
                    'license': 'UNKNOWN',  # You can enhance by fetching license data using API
                    'detection_time': detection_time
                })

        # Display the frame
        cv2.imshow('Vehicle Detection', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Store data in a JSON file
    with open('C:/Users/Vicky/Traffic-analysis/vehicle_data.json', 'w') as json_file:
        json.dump(vehicle_data, json_file, indent=4)

# Path to the video
video_path = 'parking.mp4'
extract_vehicle_details(video_path)


# Path to the pre-trained Haar Cascade classifier for vehicle detection
vehicle_cascade_path = cv2.data.haarcascades + 'haarcascade_car.xml'

# Check if the file exists
print(f"Classifier path: {vehicle_cascade_path}")

# Load the classifier
vehicle_cascade = cv2.CascadeClassifier(vehicle_cascade_path)

# Check if the classifier is empty
if vehicle_cascade.empty():
    print("Error: Haar Cascade classifier is empty. The file could not be loaded.")
else:
    print("Haar Cascade classifier loaded successfully.")
