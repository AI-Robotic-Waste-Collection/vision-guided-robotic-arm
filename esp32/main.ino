#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver servoDriver = Adafruit_PWMServoDriver(0x40);

// PCA9685 channels
const int BASE_SERVO = 0;
const int SHOULDER_SERVO = 1;
const int ELBOW_SERVO = 2;
const int GRIPPER_SERVO = 3;

// Servo pulse limits
const int SERVO_MIN = 150;
const int SERVO_MAX = 600;

// Serial input
String incomingData = "";

// Home position
int baseAngle = 90;
int shoulderAngle = 90;
int elbowAngle = 90;
int gripperAngle = 90;


void setServo(int channel, int angle)
{
  angle = constrain(angle, 0, 180);

  int pulse = map(
    angle,
    0,
    180,
    SERVO_MIN,
    SERVO_MAX
  );

  servoDriver.setPWM(channel, 0, pulse);
}


void moveArmHome()
{
  setServo(BASE_SERVO, baseAngle);
  setServo(SHOULDER_SERVO, shoulderAngle);
  setServo(ELBOW_SERVO, elbowAngle);
  setServo(GRIPPER_SERVO, gripperAngle);
}


void processGridCommand(String command)
{
  command.trim();

  if (command.length() != 2)
  {
    return;
  }

  char column = command.charAt(0);
  char row = command.charAt(1);

  if (
    (column != 'L' && column != 'C' && column != 'R') ||
    (row != '1' && row != '2' && row != '3')
  )
  {
    return;
  }

  Serial.print("Received position: ");
  Serial.println(command);

  // Basic grid-to-base mapping.
  // These values are starting points and must be
  // calibrated with the physical robotic arm.

  if (column == 'L')
  {
    baseAngle = 80;
  }
  else if (column == 'C')
  {
    baseAngle = 90;
  }
  else if (column == 'R')
  {
    baseAngle = 100;
  }

  setServo(BASE_SERVO, baseAngle);

  Serial.print("Base angle: ");
  Serial.println(baseAngle);

  // Shoulder, elbow and gripper movement will be
  // added after physical calibration.

  Serial.println("DONE");
}


void setup()
{
  Serial.begin(115200);

  Wire.begin();

  servoDriver.begin();
  servoDriver.setPWMFreq(50);

  delay(500);

  moveArmHome();

  Serial.println("ESP32 robotic arm controller started.");
  Serial.println("Waiting for grid position...");
}


void loop()
{
  while (Serial.available())
  {
    char character = Serial.read();

    if (character == '\n')
    {
      processGridCommand(incomingData);
      incomingData = "";
    }
    else if (character != '\r')
    {
      incomingData += character;
    }
  }
}
