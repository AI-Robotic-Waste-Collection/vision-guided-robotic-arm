# AI-Based Autonomous Robotic Waste Collection System

This is an academic AI and Robotics project focused on building a robotic system that can detect and collect waste with as little human involvement as possible.

## Project Overview

The system uses a camera to look at a table and a custom-trained YOLO model to detect a target waste object.

Once an object is detected, the system finds its position within the camera view and divides the working area into a simple 3 × 3 grid. The detected position is then sent to an ESP32 through serial communication.

The ESP32 uses this information to control a 4-DOF robotic arm through a PCA9685 servo driver. The arm can then move toward the detected object and use its gripper to pick it up.

The main idea is to connect **AI-based vision with physical robotic movement** so the robot can make decisions based on what the camera sees.

## How the System Works

```text
Camera
   ↓
OpenCV
   ↓
YOLO Object Detection
   ↓
Find Object Position
   ↓
3 × 3 Grid Position
   ↓
Serial Communication
   ↓
ESP32-S3
   ↓
PCA9685
   ↓
4-DOF Robotic Arm
   ↓
Gripper
   ↓
Waste Collection
```

## Technologies Used

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

## Computer Vision

The computer vision part is responsible for understanding what the camera sees.

The system:

1. Captures video from the camera.
2. Uses the trained YOLO model to look for the target waste object.
3. Finds the center of the detected object.
4. Checks which section of the working area contains the object.
5. Waits for the detection to remain stable.
6. Converts the position into a grid command.
7. Sends the command to the ESP32.
8. Waits for the robotic system to complete its movement.

The main program is:

`computer-vision/trash_detection.py`

The trained YOLO model is:

`computer-vision/best.pt`

## 3 × 3 Working Area

To make communication between the vision system and the robotic arm simpler, the reachable area is divided into nine sections:

```text
L1 | C1 | R1
---+----+---
L2 | C2 | R2
---+----+---
L3 | C3 | R3
```

For example, if the detected object is in the centre of the table, the computer vision system can send the `C2` position to the ESP32.

## ESP32 and Robotic Arm

The ESP32 acts as the connection between the computer vision system and the physical robot.

It receives the position command from the computer through serial communication and uses the PCA9685 servo driver to control the robotic arm's servo motors.

This allows the computer vision system to identify **where the object is**, while the ESP32 handles **how the robotic arm moves**.

## Current Development Status

### Completed

* Custom YOLO model training
* Camera-based object detection
* Object position detection
* 3 × 3 workspace grid
* Detection stability checking
* Computer-to-ESP32 serial communication
* ESP32 robotic control
* PCA9685 servo control
* 4-DOF robotic arm control
* Gripper control

### Still Being Developed

* Camera-to-robot coordinate calibration
* More accurate object positioning
* Reliable physical pick-and-place movement
* Testing with different object positions
* Testing under different lighting conditions
* System performance evaluation
* Final experimental testing and documentation

## Running the Computer Vision Program

Open a terminal in the `computer-vision` folder and install the required Python packages:

```bash
pip install -r requirements.txt
```

Make sure the ESP32 is connected and that the serial port configured in `trash_detection.py` matches the port being used.

Then run:

```bash
python trash_detection.py
```

## Project Goal

The goal of this project is to explore how artificial intelligence and robotics can work together to automate a simple real-world task.

Instead of simply detecting an object on a screen, the project connects the AI detection directly to a physical robotic system.

The overall process is:

**See → Detect → Locate → Decide → Move → Pick**

## Author

AI & Robotics Research Project

Sri Lanka
