# AI Model: Smart Bin Waste Classifier

The computer vision model behind the AI smart bin. It uses a camera to classify waste into three categories (**recycling**, **general** and **compost**) and tells the bin which lid to open. 

Led by Oliver Flynn as part of the [Trash-E Smart Bin](../README.md) project.

## Overview
- **Data:** collected our own photos of real waste items to train our model.
- **Training:** trained a custom YOLOv8 object detection model in Google Colab (30 epochs, batch size 16, 640x640 images), the final model was built from fine-tuning from our previous versions of the models.
- **Detection script:** wrote the Python script that runs the model on a live camera feed and picks the most confident.
- **Stability check:** an item must be detected with at least 70% confidence for 0.5 seconds before it counts. This stops the lid opening on a one-frame misdetection.
- **Hardware link:** the Raspberry Pi sends a single letter over USB serial (`R`, `G` or `C`) to an Arduino, which opens the matching lid. A signal is sent once per item and resets when the item leaves the camera's view.
- **Deployment:** exported the model to ONNX for faster inference on the Raspberry Pi, and built a separate webcam version so the model could be tested on a Windows PC without the bin.

## How it works
```
Pi camera -> YOLOv8 (ONNX) on Raspberry Pi -> Arduino -> lid
```

The model classifies items into three classes: `compost`, `general` and `recycling`.

## Folders

| Folder | Contents |
|---|---|
| `raspberry-pi/` | The version used in the bin: `start.py` and `best.onnx` |
| `windows/` | Webcam testing version: `start.py` and `best.pt`. It has no Arduino or Pi code, so it can run on a normal PC. It uses the same trained model as the Pi version |

## Development history
- **Pre-trained models:** the first prototype used off-the-shelf models (not included in this repository). However this model proved to be insufficent at detectinf a wide variety of waste and could only detect plastic cups or bottles.
- **First custom model:** Instead we trained our own model, with a Windows webcam test version and a Raspberry Pi version to be tested with the bin.
- **Expanded recycling:** to expand the model we added new recycling items (such as: egg carton, beans tin, milk). Retrained with 100s of new general waste images and 80 new compost images of existing items.
- **Final model:** added 3 new compost items to strengthen compost detection (apple, orange, onion). Added "null" training data of the room and background, and retrained with more general waste images. Exported to ONNX for the Raspberry Pi. This is the model included here.

## Tools
Python, Ultralytics YOLOv8, OpenCV, ONNX, Picamera2, PySerial, Raspberry Pi, Arduino, Google Colab, Roboflow

## Data
Trained on our own photos of real-world waste items. The dataset is not included in this repository.

## Run it

**Important: the model path in each `start.py` is left blank. You must edit it to point to the model file on your own machine before running.**

**On the Raspberry Pi (full system):**
1. Connect the Pi camera and the Arduino (USB serial).
2. Install the requirements: Ultralytics, OpenCV, PySerial and Picamera2.
3. Open `raspberry-pi/start.py` and set the path to `best.onnx`, for example:
```python
MODEL_PATH = "best.onnx"
```
4. Run it:
```
python start.py
```
5. Press `q` in the video window to quit.

**On a PC (Windows, webcam only):**
1. Open `windows/start.py` and set the path to `best.pt` on the line that loads the model, for example:
```python
model = YOLO(r"best.pt")
```
2. Run `python start.py`. It uses your webcam.
3. Press `s` to save a raw frame (used to collect "null" training images) and `q` to quit.

If the model file is in the same folder as the script, the file name alone is enough. Otherwise use the full path.

## Limitations
- The model was trained on a fixed set of items, so it isn't expected to work on any waste item.
- `start.py` covers AI detection only. The barcode fallback is separate and requires internet.
- `raspberry-pi/start.py` needs Raspberry Pi hardware (Picamera2) and an Arduino on `/dev/ttyUSB0`.
- The Arduino lid-control code is not part of this folder.
