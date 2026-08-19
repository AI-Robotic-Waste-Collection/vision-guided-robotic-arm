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

String incomingData = "";

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


void processDetection(String data)
{
  data.trim();

  if (!data.startsWith("DETECTED,"))
  {
    return;
  }

  // Remove "DETECTED,"
  data.remove(0, 9);

  int firstComma = data.indexOf(',');

  if (firstComma == -1)
  {
    return;
  }

  String objectName = data.substring(0, firstComma);

  data.remove(0, firstComma + 1);

  int secondComma = data.indexOf(',');

  if (secondComma == -1)
  {
    return;
  }

  int x = data.substring(0, secondComma).toInt();
  int y = data.substring(secondComma + 1).toInt();

  Serial.print("Object: ");
  Serial.println(objectName);

  Serial.print("X: ");
  Serial.println(x);

  Serial.print("Y: ");
  Serial.println(y);

  Serial.println("--------------------");

  /*
    Camera coordinates are not servo angles.

    For now we only use them as a basic reference.
    The actual camera-to-arm calibration will be added
    after we test the physical arm.
  */

  if (x < 250)
  {
    baseAngle = 80;
  }
  else if (x > 390)
  {
    baseAngle = 100;
  }
  else
  {
    baseAngle = 90;
  }

  setServo(BASE_SERVO, baseAngle);
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
  Serial.println("Waiting for object detection...");
}


void loop()
{
  while (Serial.available())
  {
    char character = Serial.read();

    if (character == '\n')
    {
      processDetection(incomingData);
      incomingData = "";
    }
    else
    {
      incomingData += character;
    }
  }
}
