python
from pathlib import Path
from typing import Optional
import time

import cv2
import serial
from serial import SerialException
from ultralytics import YOLO


# Model file
MODEL_PATH = Path(__file__).parent / "best.pt"


# ESP32 settings
SERIAL_PORT = "COM7"
BAUD_RATE = 115200
ROBOT_TIMEOUT_SECONDS = 60.0


# Camera settings
CAMERA_INDEX = 1
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

CONFIDENCE_THRESHOLD = 0.50

REQUIRED_STABLE_FRAMES = 8
REQUIRED_MISSING_FRAMES = 20


def wait_for_robot(
    esp32: serial.Serial,
    timeout: float = ROBOT_TIMEOUT_SECONDS,
) -> bool:
    start_time = time.time()

    while time.time() - start_time < timeout:
        if esp32.in_waiting > 0:
            message = (
                esp32.readline()
                .decode("utf-8", errors="ignore")
                .strip()
            )

            if message:
                print(f"ESP32: {message}")

            if message == "DONE":
                print("Robot completed the movement.")
                return True

        time.sleep(0.05)

    print("WARNING: Robot did not report DONE.")
    return False


def open_serial_connection() -> Optional[serial.Serial]:
    try:
        esp32 = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=0.1,
            write_timeout=1,
        )

        # Give the ESP32 a moment to restart after connecting.
        time.sleep(2)

        esp32.reset_input_buffer()

        print(f"Connected to ESP32 on {SERIAL_PORT}")
        return esp32

    except SerialException as error:
        print(f"ERROR: Could not open {SERIAL_PORT}")
        print(error)
        print("Close Arduino Serial Monitor and try again.")
        return None


def send_command(
    esp32: serial.Serial,
    command: str,
) -> bool:
    try:
        esp32.write(
            f"{command}\n".encode("utf-8")
        )

        esp32.flush()

        print(f"Sent to ESP32: {command}")
        return True

    except SerialException as error:
        print("ERROR: Could not send command to ESP32.")
        print(error)
        return False


def open_camera() -> Optional[cv2.VideoCapture]:
    print(f"Opening camera index {CAMERA_INDEX}...")

    camera = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_DSHOW,
    )

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH,
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT,
    )

    camera.set(
        cv2.CAP_PROP_FPS,
        30,
    )

    time.sleep(1)

    if not camera.isOpened():
        print(
            f"ERROR: Camera index {CAMERA_INDEX} could not open."
        )
        print("Try CAMERA_INDEX = 0, 1, 2, or 3.")
        return None

    success, frame = camera.read()

    if not success or frame is None:
        print("ERROR: Camera opened but no frame was received.")
        camera.release()
        return None

    print(f"Camera index {CAMERA_INDEX} opened successfully.")
    return camera


def main() -> None:
    if not MODEL_PATH.exists():
        print("ERROR: Model file was not found:")
        print(MODEL_PATH)
        print()
        print("Make sure best.pt is inside the computer-vision folder.")
        return

    print("Loading the YOLO model...")

    try:
        model = YOLO(str(MODEL_PATH))
    except Exception as error:
        print("ERROR: Could not load the YOLO model.")
        print(error)
        return

    print("YOLO model loaded successfully.")

    esp32 = open_serial_connection()

    if esp32 is None:
        return

    camera = open_camera()

    if camera is None:
        esp32.close()
        return

    stable_cell: Optional[str] = None
    stable_frames = 0
    missing_frames = 0
    armed = True

    print()
    print("Smart Table Robot is ready.")
    print("Press Q inside the camera window to stop.")
    print()

    try:
        while True:
            success, frame = camera.read()

            if not success or frame is None:
                print("WARNING: Could not read camera frame.")
                time.sleep(0.1)
                continue

            frame = cv2.resize(
                frame,
                (CAMERA_WIDTH, CAMERA_HEIGHT),
            )

            height, width = frame.shape[:2]

            # Define the area that the robot can reach.
            roi_left = int(width * 0.15)
            roi_right = int(width * 0.85)
            roi_top = int(height * 0.15)
            roi_bottom = int(height * 0.85)

            grid_width = (
                roi_right - roi_left
            ) / 3

            grid_height = (
                roi_bottom - roi_top
            ) / 3

            # Run the object detector.
            results = model.predict(
                source=frame,
                conf=CONFIDENCE_THRESHOLD,
                imgsz=640,
                verbose=False,
            )

            result = results[0]
            display_frame = result.plot()

            detected_cell: Optional[str] = None
            best_confidence = 0.0

            boxes = result.boxes

            if boxes is not None and len(boxes) > 0:
                confidence_values = (
                    boxes.conf
                    .cpu()
                    .tolist()
                )

                best_index = max(
                    range(len(confidence_values)),
                    key=confidence_values.__getitem__,
                )

                best_confidence = confidence_values[
                    best_index
                ]

                x1, y1, x2, y2 = (
                    boxes.xyxy[best_index]
                    .cpu()
                    .tolist()
                )

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                inside_reachable_area = (
                    roi_left <= center_x < roi_right
                    and roi_top <= center_y < roi_bottom
                )

                if inside_reachable_area:
                    column = int(
                        (center_x - roi_left)
                        / grid_width
                    )

                    row = int(
                        (center_y - roi_top)
                        / grid_height
                    )

                    column = max(0, min(2, column))
                    row = max(0, min(2, row))

                    column_names = ["L", "C", "R"]
                    row_names = ["1", "2", "3"]

                    detected_cell = (
                        column_names[column]
                        + row_names[row]
                    )

                    cv2.circle(
                        display_frame,
                        (center_x, center_y),
                        7,
                        (255, 255, 255),
                        -1,
                    )

            # Wait for the detection to stay in the same grid cell
            # before sending a command to the robot.
            if detected_cell is not None:
                missing_frames = 0

                if detected_cell == stable_cell:
                    stable_frames += 1
                else:
                    stable_cell = detected_cell
                    stable_frames = 1

            else:
                stable_cell = None
                stable_frames = 0
                missing_frames += 1

            if (
                armed
                and stable_cell is not None
                and stable_frames >= REQUIRED_STABLE_FRAMES
            ):
                print(
                    f"Paper ball detected at {stable_cell}"
                )

                command_sent = send_command(
                    esp32,
                    stable_cell,
                )

                if command_sent:
                    armed = False
                    stable_frames = 0

                    wait_for_robot(esp32)

            # Wait until the object is gone before allowing
            # another detection.
            if (
                not armed
                and missing_frames >= REQUIRED_MISSING_FRAMES
            ):
                armed = True
                print("Ready for the next paper ball.")

            # Draw the reachable area and 3 x 3 grid.
            cv2.rectangle(
                display_frame,
                (roi_left, roi_top),
                (roi_right, roi_bottom),
                (0, 255, 0),
                2,
            )

            for index in (1, 2):
                x_position = int(
                    roi_left
                    + grid_width * index
                )

                cv2.line(
                    display_frame,
                    (x_position, roi_top),
                    (x_position, roi_bottom),
                    (0, 255, 0),
                    1,
                )

            for index in (1, 2):
                y_position = int(
                    roi_top
                    + grid_height * index
                )

                cv2.line(
                    display_frame,
                    (roi_left, y_position),
                    (roi_right, y_position),
                    (0, 255, 0),
                    1,
                )

            # Add labels to each grid cell.
            column_names = ["L", "C", "R"]

            for row_index in range(3):
                for column_index in range(3):
                    label = (
                        f"{column_names[column_index]}"
                        f"{row_index + 1}"
                    )

                    text_x = int(
                        roi_left
                        + grid_width * column_index
                        + 10
                    )

                    text_y = int(
                        roi_top
                        + grid_height * row_index
                        + 25
                    )

                    cv2.putText(
                        display_frame,
                        label,
                        (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 255, 0),
                        2,
                    )

            # Show the current robot status.
            if armed:
                status_text = (
                    f"READY | "
                    f"{stable_cell or '-'} | "
                    f"{stable_frames}/"
                    f"{REQUIRED_STABLE_FRAMES}"
                )
            else:
                status_text = "ROBOT BUSY"

            cv2.putText(
                display_frame,
                status_text,
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 255),
                2,
            )

            if best_confidence > 0:
                cv2.putText(
                    display_frame,
                    (
                        f"Confidence: "
                        f"{best_confidence:.2f}"
                    ),
                    (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2,
                )

            cv2.imshow(
                "Smart Table Robot - iPhone Camera",
                display_frame,
            )

            pressed_key = cv2.waitKey(1) & 0xFF

            if pressed_key == ord("q"):
                break

    except KeyboardInterrupt:
        print("Program stopped by user.")

    finally:
        camera.release()
        cv2.destroyAllWindows()

        if esp32.is_open:
            esp32.close()

        print("Program closed.")


if __name__ == "__main__":
    main()

