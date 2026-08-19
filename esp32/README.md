# ESP32 Robotic Arm Controller

This folder contains the ESP32 program used to control the robotic arm.

## Purpose

The ESP32 receives object detection information from the computer vision system and controls the robotic arm through a PCA9685 servo driver.

## Hardware

- ESP32-S3 development board
- PCA9685 16-channel PWM servo driver
- 4-DOF robotic arm
- Servo motors
- External 5V power supply

## Servo Channels

| Channel | Function |
|---|---|
| 0 | Base |
| 1 | Shoulder |
| 2 | Elbow |
| 3 | Gripper |

## Communication

The computer vision program sends detection information to the ESP32 through serial communication.

The current message format is:

`DETECTED,object_name,x,y`

For example:

`DETECTED,paper_ball,320,240`

The ESP32 reads the object name and the camera coordinates.

## PCA9685

The PCA9685 is used to generate the PWM signals required to control the robotic arm servos.

The PCA9685 communicates with the ESP32 using I2C.

## Current Status

The current version can receive object detection data and make a basic base-servo adjustment based on the detected object's horizontal camera position.

Camera-to-arm coordinate calibration and the complete pick-and-place sequence will be implemented during the next stage of development.
