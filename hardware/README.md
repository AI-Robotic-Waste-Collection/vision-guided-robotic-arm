# Hardware

This folder documents the physical components used to build the autonomous robotic waste collection system.

## Main Components

- ESP32-S3 development board
- PCA9685 16-channel PWM servo driver
- 4-DOF acrylic robotic arm with gripper
- MG90S servo motors
- USB-C cable
- Breadboard
- Jumper wires
- 5V power supply

## Robotic Arm

The robotic arm has four degrees of freedom:

1. Base rotation
2. Shoulder movement
3. Elbow movement
4. Gripper movement

The servos are controlled through the PCA9685 servo driver.

## Servo Driver

The PCA9685 provides separate PWM channels for controlling the arm servos.

Current channel assignment:

| PCA9685 Channel | Servo |
|---|---|
| 0 | Base |
| 1 | Shoulder |
| 2 | Elbow |
| 3 | Gripper |

## Power

The servo motors are powered from an external 5V supply rather than directly from the ESP32.

The ESP32 and PCA9685 share a common ground so that the control signals have a common reference.

## Communication

The ESP32 communicates with the computer vision system through USB serial communication.

The computer runs the YOLO object detection system, while the ESP32 is responsible for receiving commands and controlling the robotic arm.

## Development Status

The hardware is being developed and tested together with the computer vision and control software.

Servo positions, movement limits, and camera-to-arm calibration will be adjusted during physical testing.
