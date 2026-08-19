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

```text
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
