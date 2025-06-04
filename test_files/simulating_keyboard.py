import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_direction = None  # to avoid pressing keys repeatedly

while True:
    success, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    right_hand_y = None
    left_hand_y = None

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            label = handedness.classification[0].label
            wrist_y = hand_landmarks.landmark[0].y

            if label == "Left":
                right_hand_y = wrist_y
            elif label == "Right":
                left_hand_y = wrist_y

        if left_hand_y is not None and right_hand_y is not None:
            diff = abs(left_hand_y - right_hand_y)

            if diff < 0.2:
                direction = "Straight"
            elif left_hand_y < right_hand_y:
                direction = "Turn Right"
            else:
                direction = "Turn Left"

            # Show info
            text = f"{direction} | Δy = {diff:.3f}"
            cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            print(text)

            # Send keyboard input
            if direction != last_direction:
                # Release all keys before switching
                keyboard.release(Key.left)
                keyboard.release(Key.right)

                if direction == "Turn Left":
                    keyboard.press(Key.left)
                elif direction == "Turn Right":
                    keyboard.press(Key.right)
                # No key press for Straight

                last_direction = direction

    cv2.imshow("Steering Simulation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
keyboard.release(Key.left)
keyboard.release(Key.right)
cap.release()
cv2.destroyAllWindows()
