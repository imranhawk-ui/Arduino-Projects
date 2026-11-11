
# Gesture-based human-machine interaction
# MediaPipe + OpenCV + Arduino Uno

import cv2
import mediapipe as mp
import serial
import time

# --------------------------------
# 1. Connect to Arduino
# --------------------------------

arduino = serial.Serial('COM3', 9600, timeout=1)

time.sleep(2)

last_command = None

print("Arduino connected!")

# --------------------------------
# 2. Start camera
# --------------------------------

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

# MediaPipe Tasks API
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
Options = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

# Hand landmark connections
connections = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

options = Options(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)

# --------------------------------
# 3. Finger detection function
# --------------------------------

def count_fingers(hand, width, height):

    fingers = {}

    # Right thumb detection
    thumb_tip = hand[4]
    thumb_ip = hand[3]
    thumb_mcp = hand[2]

    fingers["Thumb"] = (
        abs(thumb_tip.x - thumb_mcp.x) >
        abs(thumb_ip.x - thumb_mcp.x)
    )

    # Other four fingers
    finger_data = {
        "Index": (8, 6),
        "Middle": (12, 10),
        "Ring": (16, 14),
        "Little": (20, 18)
    }

    for name, (tip, joint) in finger_data.items():
        fingers[name] = hand[tip].y < hand[joint].y

    return fingers


# --------------------------------
# 4. Main detection loop
# --------------------------------

try:

    with HandLandmarker.create_from_options(options) as detector:

        start_time = time.time()

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            height, width, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp = int((time.time() - start_time) * 1000)

            result = detector.detect_for_video(
                mp_image, timestamp
            )

            if result.hand_landmarks:

                for hand in result.hand_landmarks:

                    points = []

                    for landmark in hand:

                        x = int(landmark.x * width)
                        y = int(landmark.y * height)

                        points.append((x, y))

                        cv2.circle(
                            frame, (x, y), 5,
                            (0, 255, 0), -1
                        )

                    for start, end in connections:

                        cv2.line(
                            frame,
                            points[start],
                            points[end],
                            (255, 0, 0), 2
                        )

                    # Detect fingers
                    fingers = count_fingers(
                        hand, width, height
                    )

                    count = 0

                    for i, (name, is_open) in enumerate(fingers.items()):

                        status = "OPEN" if is_open else "CLOSED"

                        if is_open:
                            count += 1

                        cv2.putText(
                            frame,
                            name + ": " + status,
                            (20, 50 + i * 35),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0) if is_open else (0, 0, 255),
                            2
                        )

                    # --------------------------------
                    # 5. Send finger states to Arduino
                    # --------------------------------

                    finger_order = [
                        "Thumb",
                        "Index",
                        "Middle",
                        "Ring",
                        "Little"
                    ]

                    command = "".join(
                        "1" if fingers[name] else "0"
                        for name in finger_order
                    )

                    if command != last_command:

                        arduino.write(
                            (command + "\n").encode()
                        )

                        last_command = command

                    cv2.putText(
                        frame,
                        "Fingers Open: " + str(count),
                        (20, 250),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (255, 255, 0), 2
                    )

                    cv2.putText(
                        frame,
                        "Arduino: " + command,
                        (20, 290),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 0), 2
                    )

            else:

                # No hand detected: switch off all LEDs
                if last_command != "00000":

                    arduino.write(b"00000\n")
                    last_command = "00000"

                cv2.putText(
                    frame,
                    "No Hand Detected",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255), 2
                )

            cv2.imshow("Finger Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:

    # Switch off all LEDs when program exits
    if arduino.is_open:
        arduino.write(b"00000\n")
        arduino.close()

    cap.release()
    cv2.destroyAllWindows()

    print("Program closed.")
