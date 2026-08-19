# AI-Based Autonomous Robotic Waste Collection System

An academic research project exploring artificial intelligence, computer vision, and robotic manipulation for autonomous waste collection.

## Project Overview

This project uses a camera and a custom-trained YOLO object detection model to identify waste objects on a table.

When an object is detected, its position is sent to an ESP32. The ESP32 controls a 4-DOF robotic arm through a PCA9685 servo driver.

The goal is to develop a system that can detect, locate, pick up, and collect waste with minimal human intervention.

## Technologies

- Python
- OpenCV
- YOLO
- NumPy
- PySerial
- ESP32-S3
- PCA9685
- Arduino/C++

## Project Structure

AI-Robotic-Waste-Collection/
│
├── computer-vision/
│   ├── main.py
│   ├── README.md
│   └── requirements.txt
│
├── esp32/
│   ├── main.ino
│   └── README.md
│
├── hardware/
│   └── README.md
│
├── .gitignore
└── README.md

## System Workflow

Camera
↓
YOLO Object Detection
↓
Object Position
↓
ESP32
↓
PCA9685
↓
Robotic Arm
↓
Waste Collection

## Current Status

The project is currently under development.

Implemented:

- YOLO-based object detection
- Camera input
- Computer-to-ESP32 serial communication
- PCA9685 servo control
- Basic robotic arm control

Still under development:

- Camera-to-arm calibration
- Accurate object positioning
- Pick-and-place movement
- Gripper control
- Full autonomous operation
- Physical testing and evaluation

## Author

AI & Robotics Research Project  
Sri Lanka
