import cv2
from ultralytics import YOLO
import os
import time

#path to best.pt file
model = YOLO(r"")

#Opens the webcam
cap = cv2.VideoCapture(0)

#Folder to save null screenshots
os.makedirs('null_captures', exist_ok=True)
screenshot_count = 0

#Stability tracking
STABILITY_THRESHOLD = 0.5  
stable_class = None
stable_start = None
confirmed_class = None

#Starts Webcam
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=0.7)

    current_class = None
    if results[0].boxes:
        best_box = max(results[0].boxes, key=lambda b: b.conf)
        current_class = results[0].names[int(best_box.cls)]

    #Stability logic
    if current_class == stable_class and current_class is not None:
        if time.time() - stable_start >= STABILITY_THRESHOLD:
            confirmed_class = stable_class
    else:
        stable_class = current_class
        stable_start = time.time()
        if current_class is None:
            confirmed_class = None

    #Shows the results on screen
    annotated_frame = results[0].plot()
    cv2.imshow("Trash Detector V3", annotated_frame)

    key = cv2.waitKey(1) & 0xFF

    #Press S to save raw frame without boxes
    if key == ord('s'):
        filename = f'null_captures/null_{screenshot_count}.jpg'
        cv2.imwrite(filename, frame)
        screenshot_count += 1
        print(f'Saved null_{screenshot_count}.jpg')

    #Breaks the loop if 'q' is pressed
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()