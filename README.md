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


![image](https://github.com/user-attachments/assets/be73c066-0ddf-4b0b-9124-c6f1e6a75df0)



**Steps:**

✅ Step 1 – Installed Required Libraries

    pip install opencv-python mediapipe pyautogui keyboard

✅ Step 2 – Created a Python Script to Open the Camera

   camera_test.py

✅ Step 3 – Created a Python Script to Detect Hands 

   mediapipe_test.py

✅ Step 4 – Use Hand Landmarks to Detect Left or Right Movement

   Use the position of my hand to decide if I’m turning left, right, or center — so later we can control steering in the game.

   turning_test.py












   
