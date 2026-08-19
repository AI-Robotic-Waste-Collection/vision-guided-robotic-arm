# AI-Based Vision-Guided Autonomous Robotic Arm for Waste Collection

An academic research project investigating the use of artificial intelligence, computer vision, and robotic manipulation for autonomous tabletop waste collection.

## Project Overview

This project develops a robotic system capable of detecting waste objects using a camera, identifying their location using a YOLO-based computer vision model, and controlling a robotic arm to pick up the detected object and place it into a designated collection bin.

The system combines:

- Artificial Intelligence
- Computer Vision
- Object Detection
- Robotic Manipulation
- ESP32 Microcontroller Control
- Servo Motor Control
- Autonomous Decision Making

## System Workflow

Camera
↓
Image Capture
↓
YOLO Object Detection
↓
Object Location
↓
Movement Decision
↓
ESP32
↓
PCA9685 Servo Driver
↓
Robotic Arm
↓
Gripper
↓
Waste Collection Bin

## Hardware

- ESP32-S3 development board
- PCA9685 16-channel PWM servo driver
- 4-DOF acrylic robotic arm
- MG90S servo motors
- Robotic gripper
- External 5V power supply
- USB-C cable
- Computer for computer-vision processing
- Camera
- Collection bin

## Software

- Python
- OpenCV
- Ultralytics YOLO
- PySerial
- Arduino IDE
- ESP32 Arduino framework

## AI Model

The project uses a YOLO object-detection model trained on a custom dataset.

The model is designed to detect the target waste object and provide its bounding-box coordinates to the robotic-control system.

The trained model is stored separately from the source code.

## Project Structure

```text
vision-guided-robotic-arm/
│
├── README.md
├── .gitignore
│
├── computer-vision/
│   ├── detection.py
│   ├── camera.py
│   ├── requirements.txt
│   └── README.md
│
├── robotic-arm/
│   └── esp32-control/
│       ├── robotic_arm.ino
│       └── README.md
│
├── model/
│   └── README.md
│
├── dataset/
│   └── README.md
│
├── experiments/
│   ├── test-results.csv
│   └── results.md
│
├── hardware/
│   ├── components.md
│   ├── wiring.md
│   └── calibration.md
│
└── docs/
    ├── project-overview.md
    ├── problem-statement.md
    ├── objectives.md
    ├── methodology.md
    ├── system-architecture.md
    ├── testing.md
    ├── limitations.md
    └── future-work.md
