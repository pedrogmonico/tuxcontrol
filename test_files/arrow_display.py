import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import numpy as np

keyboard = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_direction = None  # to avoid pressing keys repeatedly

def draw_arrow_panel(pressed_keys):
    img = np.ones((250, 320, 3), dtype=np.uint8) * 230  # light gray background

    # Key size and layout
    key_w, key_h = 70, 70
    gap = 10

    # Positions for keys (inverted T layout)
    # Center of bottom row
    center_x = img.shape[1] // 2
    center_y = img.shape[0] // 2 + 30

    # Calculate top row positions
    up_pos = (center_x, center_y - key_h - gap)
    left_pos = (center_x - key_w - gap, center_y)
    down_pos = (center_x, center_y)
    right_pos = (center_x + key_w + gap, center_y)

    def draw_key(top_left, label, pressed):
        x, y = top_left
        # Colors
        base_color = (245, 245, 245)
        pressed_color = (60, 160, 60)
        border_color = (120, 120, 120)
        shadow_color = (180, 180, 180)

        # Draw shadow (bottom right offset)
        shadow_offset = 5
        cv2.rectangle(img, (x + shadow_offset, y + shadow_offset),
                      (x + key_w + shadow_offset, y + key_h + shadow_offset), shadow_color, -1)

        # Draw key background
        color = pressed_color if pressed else base_color
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), color, -1)

        # Draw key border
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), border_color, 2)

        # Draw arrow symbol in center
        center_key = (x + key_w // 2, y + key_h // 2)
        arrow_color = (255, 255, 255) if pressed else (60, 60, 60)

        # Arrow polygons, relative to center_key
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

    # Draw all keys
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

    right_hand_y = None
    left_hand_y = None

    pressed = {'up': False, 'down': False, 'left': False, 'right': False}

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

            # Show info on webcam frame
            text = f"{direction} | Δy = {diff:.3f}"
            cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            print(text)

            # Send keyboard input and update pressed keys
            if direction != last_direction:
                keyboard.release(Key.left)
                keyboard.release(Key.right)

                if direction == "Turn Left":
                    keyboard.press(Key.left)
                    pressed['left'] = True
                elif direction == "Turn Right":
                    keyboard.press(Key.right)
                    pressed['right'] = True
                else:
                    # Straight, no keys pressed
                    pressed['left'] = False
                    pressed['right'] = False

                last_direction = direction
            else:
                # If direction hasn't changed, keep the same pressed state visually
                if direction == "Turn Left":
                    pressed['left'] = True
                elif direction == "Turn Right":
                    pressed['right'] = True

    # Draw the arrow panel with current pressed keys
    arrow_panel = draw_arrow_panel(pressed)

    # Show both windows
    cv2.imshow("Steering Simulation", frame)
    cv2.imshow("Arrow Panel", arrow_panel)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all keys on exit
keyboard.release(Key.left)
keyboard.release(Key.right)
cap.release()
cv2.destroyAllWindows()


"""
When the direction changes, it releases any previously pressed arrow keys and presses the new corresponding arrow key (left or right). The pressed dictionary tracks which keys are currently active to update the visual arrow panel, ensuring the displayed keys match the simulated keyboard inputs. 
keyboard.press(Key.right) -> This sends a real keyboard event to the computer,
"""