# AI-Based Autonomous Robotic Waste Collection System

An academic AI and Robotics research project exploring computer vision, autonomous decision-making, and robotic manipulation for automated waste collection.

## Project Overview

This project combines a camera-based computer vision system with an ESP32-controlled robotic arm to detect and collect waste objects from a defined working area.

A custom-trained YOLO object detection model identifies the target waste object in the camera feed. The detected object's position is converted into a 3 × 3 grid location and transmitted to an ESP32 through serial communication.

The ESP32 receives the position command and controls the robotic arm through a PCA9685 servo driver.

The overall goal is to create a system capable of:

* Detecting waste using artificial intelligence.
* Locating the detected object within the robot's working area.
* Communicating the target position to the robotic controller.
* Moving the robotic arm toward the detected object.
* Picking up the object using a gripper.
* Collecting the object with minimal human intervention.

## System Architecture

```text
Camera
  ↓
OpenCV Video Capture
  ↓
Custom YOLO Object Detection
  ↓
Object Position / 3 × 3 Grid
  ↓
Serial Communication
  ↓
ESP32-S3
  ↓
PCA9685 Servo Driver
  ↓
4-DOF Robotic Arm
  ↓
Gripper
  ↓
Waste Collection
```

## Technologies

### Software

* Python
* OpenCV
* Ultralytics YOLO
* NumPy
* PySerial
* Arduino IDE

### Hardware

* ESP32-S3
* PCA9685 16-channel PWM servo driver
* 4-DOF robotic arm
* Servo motors
* Robotic gripper
* Camera

## Project Structure

```text
vision-guided-robotic-arm/
│
├── computer-vision/
│   ├── README.md
│   ├── requirements.txt
│   ├── best.pt
│   └── trash_detection.py
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
```

## Computer Vision System

The computer vision subsystem uses a custom-trained YOLO model to detect the target waste object.

The detection system:

1. Captures frames from the camera.
2. Runs YOLO object detection.
3. Selects the strongest detected target.
4. Calculates the object's center position.
5. Determines which cell of the 3 × 3 reachable grid contains the object.
6. Waits for the detection to remain stable.
7. Sends the grid command to the ESP32.
8. Waits for the robot to complete its movement.

The main computer vision program is `computer-vision/trash_detection.py`.

The trained model is `computer-vision/best.pt`.

## 3 × 3 Position Grid

The reachable working area is divided into nine logical positions:

```text
L1 | C1 | R1
---+----+---
L2 | C2 | R2
---+----+---
L3 | C3 | R3
```

The detected object's center determines which grid position is sent to the ESP32.

## ESP32 Control

The ESP32 receives position commands from the computer through serial communication.

The command identifies the target grid position, allowing the ESP32 to determine the corresponding robotic arm movement.

The PCA9685 servo driver generates the PWM signals required to control the robotic arm's servo motors.

## Current Development Status

### Implemented

* Custom YOLO object detection model
* Camera-based object detection
* Object center-position calculation
* 3 × 3 workspace grid mapping
* Detection stability checking
* Computer-to-ESP32 serial communication
* ESP32 robotic control
* PCA9685 servo control
* 4-DOF robotic arm control
* Gripper control

### Remaining Development

* Camera-to-robot coordinate calibration
* Improving positional accuracy
* Reliable physical pick-and-place operation
* Testing under different lighting conditions
* Testing with different object positions and orientations
* System performance evaluation
* Full experimental evaluation and documentation

## Running the Computer Vision System

Navigate to the computer vision directory:

```bash
cd computer-vision
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Connect the ESP32 and make sure the configured serial port matches the port used by the system.

Run the main computer vision program:

```bash
python trash_detection.py
```

## Research Objective

The project investigates how artificial intelligence and robotic manipulation can be combined to automate simple waste collection tasks.

The research focuses on the interaction between:

**Artificial Intelligence → Computer Vision → Decision Making → Robotic Control → Physical Manipulation**

## Author

AI & Robotics Research Project

Sri Lanka
