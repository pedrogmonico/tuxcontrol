"""
MediaPipe gives 21 points on the hand.

| Landmark Index | Name             | Location on Hand    |
| -------------- | ---------------- | ------------------- |
| 0              | Wrist            | Base of the hand    |
| 4              | Thumb tip        | Tip of the thumb    |
| 8              | Index finger tip | Tip of index finger |
| ...            | ...              | ...                 |

For steering, we’ll focus on the wrist point (0) because it gives a good horizontal position of both hands.
"""

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

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
                right_hand_y = wrist_y  # "Left" -> right real hand
            elif label == "Right":
                left_hand_y = wrist_y   

        if left_hand_y is not None and right_hand_y is not None:
            # Calcular a diferença
            diff = abs(left_hand_y - right_hand_y)

            if diff < 0.2:
                direction = "Straight"
            elif left_hand_y < right_hand_y:
                direction = "Turn Right"
            else:
                direction = "Turn Left"

            # Mostrar a direção e a diferença
            text = f"{direction} | Δy = {diff:.3f}"
            cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            print(text)

    cv2.imshow("Steering Simulation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





"""
handedness tells which hand is being tracked (label will be either 'Left' or 'Right' depending on the hand). Get the Y-coordinate of the Wrist(0 = top of frame, 1 = bottom). Store Y-coordinate Based on Hand
The cv2.putText() function in OpenCV is used to draw text on an image—in this case, on each video frame. Frame, is the image where the text will appear. Direction, is the actual text string that will be shown, such as "Turn Right", "Turn Left", or "Straight". Parameter, (50, 50), specifies the position where the text will be placed—specifically. cv2.FONT_HERSHEY_SIMPLEX, sets the font style. 1, is the font scale. 2, defines the thickness of the text.
"""