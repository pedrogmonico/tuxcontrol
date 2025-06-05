"""
Use the distance between tip of the middle finger (landmark 12) and the wrist (landmark 0).
If this distance is small → hand closed (brake).
If this distance is large → hand open (accelerate).


"""

import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

while True:
    success, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    action = "No Right Hand Detected"

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label
            
            if label == "Left":
                draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                wrist = hand_landmarks.landmark[0]
                middle_finger_tip = hand_landmarks.landmark[12]
                
                dist = distance(wrist, middle_finger_tip)

                # You can tweak this threshold by testing on your camera
                threshold = 0.17  

                if dist < threshold:
                    action = "Brake (Hand Closed)"
                else:
                    action = "Accelerate (Hand Open)"

                cv2.putText(frame, f"{action} | Dist={dist:.3f}", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                print(f"{action} | Dist={dist:.3f}")

    cv2.imshow("Acceleration/Brake Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
