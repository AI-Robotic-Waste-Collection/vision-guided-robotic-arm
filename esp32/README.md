# Hardware

This folder documents the main hardware used to build and test the autonomous robotic waste collection system.

## Main Components

* ESP32-S3 development board
* PCA9685 16-channel PWM servo driver
* 4-DOF acrylic robotic arm with gripper
* MG90S servo motors
* USB-C cable
* Breadboard
* Jumper wires
* External 5V power supply

## Robotic Arm

The robotic arm has four degrees of freedom:

1. Base rotation
2. Shoulder movement
3. Elbow movement
4. Gripper movement

Each servo is controlled through the PCA9685 servo driver.

## PCA9685 Servo Driver

The PCA9685 provides individual PWM channels for controlling the arm's servos.

The current channel assignment is:

| PCA9685 Channel | Function |
| --------------- | -------- |
| 0               | Base     |
| 1               | Shoulder |
| 2               | Elbow    |
| 3               | Gripper  |

## Power

The servos are powered using an external 5V power supply instead of drawing their power directly from the ESP32.

The ESP32 and PCA9685 share a common ground so that the control signals have the same electrical reference.

This is important because the servos can require significantly more current than the ESP32 can safely provide.

## Communication

The computer runs the AI-based computer vision system and communicates with the ESP32 through USB serial communication.

The basic system flow is:

```text
Computer Vision
      ↓
USB Serial
      ↓
ESP32-S3
      ↓
PCA9685
      ↓
Servo Motors
      ↓
Robotic Arm
```

## Development Status

The hardware is currently being developed and tested alongside the computer vision and control software.

Servo positions, movement limits, arm movement sequences, and camera-to-arm calibration will be refined through physical testing.

The final goal is to achieve reliable detection, positioning, and pick-and-place movement with the robotic arm.
