from pathlib import Path
import time

import cv2
import serial
from serial import SerialException
from ultralytics import YOLO


# Model and connection settings
MODEL_PATH = Path(__file__).parent / "best.pt"

SERIAL_PORT = "COM3"  # Change this to your ESP32 port
BAUD_RATE = 115200

CAMERA_INDEX = 0
CONFIDENCE_THRESHOLD = 0.50


# Load the trained YOLO model
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Could not find the model: {MODEL_PATH}"
    )

model = YOLO(str(MODEL_PATH))


# Try to connect to the ESP32
try:
    esp32 = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    time.sleep(2)
    print(f"ESP32 connected on {SERIAL_PORT}")

except SerialException as error:
    esp32 = None
    print(f"Could not connect to ESP32: {error}")


# Start the camera
camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():
    raise RuntimeError("Could not open the camera.")

print("Waste detection system started.")
print("Press Q to stop.")


try:
    while True:
        success, frame = camera.read()

        if not success:
            print("Failed to read from camera.")
            break

        results = model(frame, verbose=False)

        object_found = False

        for result in results:
            for box in result.boxes:

                confidence = float(box.conf[0])

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                object_found = True

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Draw the detected object
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = f"{class_name} {confidence:.2f}"

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                # Mark the centre of the object
                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    f"X: {center_x} Y: {center_y}",
                    (x1, y2 + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2
                )

                # Send the detected object's position to the ESP32
                if esp32 is not None:
                    message = (
                        f"DETECTED,"
                        f"{class_name},"
                        f"{center_x},"
                        f"{center_y}\n"
                    )

                    try:
                        esp32.write(message.encode("utf-8"))

                    except SerialException:
                        print("ESP32 connection lost.")
                        esp32 = None

        if object_found:
            status = "OBJECT DETECTED"
        else:
            status = "SEARCHING..."

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Autonomous Waste Detection System",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()

    if esp32 is not None:
        esp32.close()

    print("System stopped.")
