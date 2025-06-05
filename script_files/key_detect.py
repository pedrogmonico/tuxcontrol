import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import numpy as np
import math

keyboard = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_steering = None
last_accel_brake = None

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def draw_arrow_panel(pressed_keys):
    img = np.ones((250, 320, 3), dtype=np.uint8) * 230

    key_w, key_h = 70, 70
    gap = 10
    center_x = img.shape[1] // 2
    center_y = img.shape[0] // 2 + 30

    up_pos = (center_x, center_y - key_h - gap)
    left_pos = (center_x - key_w - gap, center_y)
    down_pos = (center_x, center_y)
    right_pos = (center_x + key_w + gap, center_y)

    def draw_key(top_left, label, pressed):
        x, y = top_left
        base_color = (245, 245, 245)
        pressed_color = (60, 160, 60)
        border_color = (120, 120, 120)
        shadow_color = (180, 180, 180)
        shadow_offset = 5

        cv2.rectangle(img, (x + shadow_offset, y + shadow_offset),
                      (x + key_w + shadow_offset, y + key_h + shadow_offset), shadow_color, -1)
        color = pressed_color if pressed else base_color
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), color, -1)
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), border_color, 2)

        center_key = (x + key_w // 2, y + key_h // 2)
        arrow_color = (255, 255, 255) if pressed else (60, 60, 60)

        if label == "UP":
            pts = np.array([
                (center_key[0], center_key[1] - 18),
                (center_key[0] - 15, center_key[1] + 10),
                (center_key[0] + 15, center_key[1] + 10)
            ])
        elif label == "DOWN":
            pts = np.array([
                (center_key[0], center_key[1] + 18),
                (center_key[0] - 15, center_key[1] - 10),
                (center_key[0] + 15, center_key[1] - 10)
            ])
        elif label == "LEFT":
            pts = np.array([
                (center_key[0] - 18, center_key[1]),
                (center_key[0] + 10, center_key[1] - 15),
                (center_key[0] + 10, center_key[1] + 15)
            ])
        elif label == "RIGHT":
            pts = np.array([
                (center_key[0] + 18, center_key[1]),
                (center_key[0] - 10, center_key[1] - 15),
                (center_key[0] - 10, center_key[1] + 15)
            ])
        else:
            pts = np.array([])

        if pts.size > 0:
            cv2.fillPoly(img, [pts], arrow_color)

    draw_key((up_pos[0] - key_w // 2, up_pos[1] - key_h // 2), "UP", pressed_keys['up'])
    draw_key((down_pos[0] - key_w // 2, down_pos[1] - key_h // 2), "DOWN", pressed_keys['down'])
    draw_key((left_pos[0] - key_w // 2, left_pos[1] - key_h // 2), "LEFT", pressed_keys['left'])
    draw_key((right_pos[0] - key_w // 2, right_pos[1] - key_h // 2), "RIGHT", pressed_keys['right'])

    return img


while True:
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    left_hand = None
    right_hand = None
    pressed = {'up': False, 'down': False, 'left': False, 'right': False}

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            label = handedness.classification[0].label
            if label == "Left":
                right_hand = hand_landmarks  # MediaPipe mirrors hands
            elif label == "Right":
                left_hand = hand_landmarks

        ### Steering Control (Left Hand)
        if left_hand:
            left_wrist_y = left_hand.landmark[0].y
            right_wrist_y = right_hand.landmark[0].y if right_hand else None

            if right_wrist_y is not None:
                diff = abs(left_wrist_y - right_wrist_y)
                if diff < 0.15:
                    direction = "Straight"
                elif left_wrist_y < right_wrist_y:
                    direction = "Turn Right"
                else:
                    direction = "Turn Left"

                cv2.putText(frame, f"{direction} | Δy={diff:.3f}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                if direction != last_steering:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)
                    if direction == "Turn Left":
                        keyboard.press(Key.left)
                        pressed['left'] = True
                    elif direction == "Turn Right":
                        keyboard.press(Key.right)
                        pressed['right'] = True
                    last_steering = direction
                else:
                    if direction == "Turn Left":
                        pressed['left'] = True
                    elif direction == "Turn Right":
                        pressed['right'] = True

        ### Acceleration/Brake Control (Right Hand)
        if right_hand:
            wrist = right_hand.landmark[0]
            middle_tip = right_hand.landmark[12]
            dist = distance(wrist, middle_tip)
            threshold = 0.17

            if dist < threshold:
                action = "Brake"
                if last_accel_brake != "Brake":
                    keyboard.release(Key.up)
                    keyboard.press(Key.down)
                    last_accel_brake = "Brake"
                pressed['down'] = True
            else:
                action = "Accelerate"
                if last_accel_brake != "Accelerate":
                    keyboard.release(Key.down)
                    keyboard.press(Key.up)
                    last_accel_brake = "Accelerate"
                pressed['up'] = True

            cv2.putText(frame, f"{action} | dist={dist:.3f}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    arrow_panel = draw_arrow_panel(pressed)

    cv2.imshow("Gesture Driving", frame)
    cv2.imshow("Arrow Panel", arrow_panel)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

keyboard.release(Key.left)
keyboard.release(Key.right)
keyboard.release(Key.up)
keyboard.release(Key.down)
cap.release()
cv2.destroyAllWindows()
