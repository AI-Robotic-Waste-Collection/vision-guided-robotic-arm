# ESP32 Robotic Arm Controller

This folder contains the ESP32 code used to control the robotic arm and communicate with the computer vision system.

## Purpose

The ESP32 acts as the controller between the AI-based vision system and the physical robotic arm.

It receives information from the computer through serial communication and uses a PCA9685 servo driver to control the arm's servos.

## Hardware

* ESP32-S3 development board
* PCA9685 16-channel PWM servo driver
* 4-DOF robotic arm
* Servo motors
* External 5V power supply

## Servo Channels

| Channel | Function |
| ------- | -------- |
| 0       | Base     |
| 1       | Shoulder |
| 2       | Elbow    |
| 3       | Gripper  |

## Communication

The ESP32 communicates with the computer using serial communication at **115200 baud**.

The current ESP32 code expects detection messages in this format:

`DETECTED,object_name,x,y`

Example:

`DETECTED,paper_ball,320,240`

The ESP32 reads the object name and the X/Y camera coordinates.

At the current stage, the X coordinate is used to make a basic adjustment to the base servo.

## PCA9685 Servo Driver

The PCA9685 generates the PWM signals used to control the robotic arm's servo motors.

It communicates with the ESP32 through the I2C interface.

The default PCA9685 I2C address used by the program is:

`0x40`

The servo driver operates at:

`50 Hz`

## Current Status

The current version successfully initializes the ESP32 and PCA9685, receives detection information through serial communication, and makes a basic base-servo adjustment based on the detected object's horizontal position.

The following parts are still being developed:

* Camera-to-arm calibration
* Accurate X/Y to robot movement conversion
* Shoulder and elbow positioning
* Gripper movement
* Complete pick-and-place sequence
* Physical testing and calibration

This project is being developed incrementally, with the communication and basic servo control tested before implementing the complete autonomous pick-and-place process.
