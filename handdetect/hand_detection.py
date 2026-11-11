
import cv2
import mediapipe as mp
import time

# Connect to DroidCam
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

# MediaPipe Tasks
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

# Model location
model_path = "hand_landmarker.task"

# Create hand detector
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Connections between hand landmarks
connections = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

with HandLandmarker.create_from_options(options) as detector:

    print("Hand detection started!")

    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received")
            break

        # Convert frame to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # Timestamp for video processing
        timestamp = int((time.time() - start_time) * 1000)

        # Detect hand
        result = detector.detect_for_video(
            mp_image, timestamp
        )

        # Draw landmarks
        if result.hand_landmarks:

            for hand in result.hand_landmarks:

                points = []

                for landmark in hand:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    points.append((x, y))

                    cv2.circle(
                        frame, (x, y), 5,
                        (0, 255, 0), -1
                    )

                # Draw connections
                for start, end in connections:
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 0, 0),
                        2
                    )

                cv2.putText(
                    frame, "Hand Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2
                )

        cv2.imshow("Hand Landmark Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
