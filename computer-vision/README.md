# Computer Vision System

This folder contains the computer vision software for the autonomous robotic waste collection system.

## Purpose

The system uses a camera and a YOLO object detection model to identify waste objects on a table.

When a target object is detected, the detected object's position is used to guide the robotic arm.

## Main Technologies

- Python
- OpenCV
- Ultralytics YOLO
- NumPy
- PySerial

## System Workflow

1. Capture video from the camera.
2. Detect waste objects using the trained YOLO model.
3. Identify the position of the detected object.
4. Send the required movement information to the ESP32.
5. The ESP32 controls the robotic arm.
6. The robotic arm picks up the detected waste.

## Files

- `main.py` — Main computer vision program.
- `best.pt` — Trained YOLO model.
- `requirements.txt` — Required Python packages.

## Installation

Install the required Python packages using:

```bash
pip install -r requirements.txt
