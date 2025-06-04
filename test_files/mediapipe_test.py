import cv2
import mediapipe as mp

# Load MediaPipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()  # Default: detects 2 hands
draw = mp.solutions.drawing_utils  # To draw landmarks

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = hands.process(frame_rgb)  # Detect hands

    # If hands are found
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show webcam feed with hand landmarks
    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()


"""
It initializes MediaPipe’s hand tracking model with mp.solutions.hands, which provides the Hands class for detecting hand landmarks. By default, this model can detect up to two hands in a video frame. An instance of this hand model is created with hands = mp_hands.Hands(). The drawing_utils module from MediaPipe is also loaded into draw, which will be used to visually mark hand landmarks on the video frames.

OpenCV captures images in BGR color format, but MediaPipe expects RGB, so the frame is converted with cv2.cvtColor().

The RGB frame is then passed to hands.process(), which runs the hand detection algorithm and returns any detected hand landmarks. If hands are detected (results.multi_hand_landmarks is not None), the script iterates through each detected hand and uses draw.draw_landmarks() to overlay the hand keypoints and their connections on the original frame. (If MediaPipe detects one or more hands, for each hand it draws the dots and lines connecting those dots on the webcam frame for you to see on the screen.)
"""