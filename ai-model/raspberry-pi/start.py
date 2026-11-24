import cv2
import numpy as np
import time
import serial
from ultralytics import YOLO
from picamera2 import Picamera2

MODEL_PATH = "" #path to best.onnx
print(f"Loading YOLOv8 ONNX model from {MODEL_PATH}...")

model = YOLO(MODEL_PATH, task="detect")

# Initialize Arduino
print("Initializing Arduino...")
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# -----------------------------------------------
# PICAMERA2 SECTION - Do not modify
print("Initializing Picamera2...")
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()
print("Camera started successfully. Press 'q' in the window to exit.")
# -----------------------------------------------

# Stability tracking
STABILITY_THRESHOLD = 0.5
stable_class = None
stable_start = None
confirmed_class = None
last_confirmed = None

try:
    while True:

        # -----------------------------------------------
        # PICAMERA2 SECTION - Do not modify
        frame = picam2.capture_array()
        frame = frame[:, :, :3]
        results = model(frame, verbose=False, conf=0.7)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 ONNX Object Detection", annotated_frame)
        # -----------------------------------------------

        # Get highest confidence detection this frame
        current_class = None
        if results[0].boxes:
            best_box = max(results[0].boxes, key=lambda b: b.conf)
            current_class = results[0].names[int(best_box.cls)]

        # Stability logic - only confirm after 0.5s of same class
        if current_class == stable_class and current_class is not None:
            if time.time() - stable_start >= STABILITY_THRESHOLD:
                confirmed_class = stable_class
        else:
            stable_class = current_class
            stable_start = time.time()
            if current_class is None:
                confirmed_class = None
                last_confirmed = None  # Reset so next item can trigger again

        # Send signal only when confirmed class changes
        if confirmed_class is not None and confirmed_class != last_confirmed:

            if confirmed_class == 'recycling':
                #SendRecyclingSignal
                arduino.write(b'R')
                print("Sent: Recycling")

            elif confirmed_class == 'general':
                #SendGeneralSignal
                arduino.write(b'G')
                print("Sent: General")

            elif confirmed_class == 'compost':
                #SendCompostSignal
                arduino.write(b'C')
                print("Sent: Compost")

            last_confirmed = confirmed_class

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # -----------------------------------------------
    # PICAMERA2 SECTION - Do not modify
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera stopped and resources cleaned up.")
    # -----------------------------------------------
    arduino.close()
    print("Arduino disconnected.")