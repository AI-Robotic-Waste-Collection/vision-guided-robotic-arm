# Computer Vision System

This folder contains the computer vision software for the autonomous robotic waste collection system.

## Purpose

The computer vision system uses a camera and a custom-trained YOLO object detection model to identify target waste objects on a table.

When a target object is detected, the system determines its location in the camera frame and communicates the detection information to the ESP32. The ESP32 then controls the robotic arm to perform the required movement.

## Main Technologies

- Python
- OpenCV
- Ultralytics YOLO
- NumPy
- PySerial
- ESP32

## System Workflow

Camera
↓
OpenCV Video Capture
↓
YOLO Object Detection
↓
Target Detection & Position
↓
Serial Communication
↓
ESP32
↓
PCA9685 Servo Driver
↓
Robotic Arm
↓
Gripper

## Files

- `trash_detection.py` — Main computer vision program.
- `best.pt` — Custom-trained YOLO model used for waste detection.
- `requirements.txt` — Python dependencies required to run the computer vision system.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt