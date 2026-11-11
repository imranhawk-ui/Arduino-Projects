#prototype demonstrating gesture-based human–machine interaction using computer vision and embedded systems.
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
Options = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

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

def count_fingers(hand, width, height):

    fingers = {}

    # Right thumb: compare horizontal positions
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

                fingers = count_fingers(hand, width, height)

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

                cv2.putText(
                    frame,
                    "Fingers Open: " + str(count),
                    (20, 250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 0), 2
                )

        cv2.imshow("Finger Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
