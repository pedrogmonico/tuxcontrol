# TuxControl
Control SuperTuxKart with Hands and Feet

🧠 Technologies Used in the Project

1. Python 🐍
   
   Simple to write and understand
   Has powerful libraries like OpenCV, MediaPipe, and pyautogui
   Perfect for connecting webcam input with game control

2. OpenCV (Open Source Computer Vision Library) 📷

    A library for real-time image and video processing. It can:
      Capture video from your webcam
      Process each frame
      Convert color formats (e.g., BGR to RGB)
      Draw shapes and landmarks on the video
   
   It’s how we access the webcam and display what it sees. It gives us the video feed needed for gesture recognition.

3. MediaPipe (by Google) 🧠✋🦶

    A powerful framework for real-time AI-powered tracking, including:
      Hand tracking
      Face mesh
      Body/pose tracking

4. PyAutoGUI ⌨️

     A Python library for controlling your keyboard and mouse programmatically.


         👁️ Webcam (via OpenCV)
                 ↓
     Frame-by-frame video captured
                 ↓
       Analyzed using MediaPipe
      ↙️                           ↘️
 Detect hand                 Detect pose
  (x-position)              (heel y-position)
      ↓                           ↓
pyautogui sends key    pyautogui sends key
 press ← or →            press ↑ or ↓
      ↓                           ↓
   Game receives simulated key press
             ↓
     Your body controls the game!




**Steps for dev:**

✅ Step 1 – Install Required Libraries

    pip install opencv-python mediapipe pyautogui keyboard

