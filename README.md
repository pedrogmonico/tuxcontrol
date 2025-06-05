# TuxControl
Control SuperTuxKart with Hands 

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

4. pynput ⌨️

     A Python library for controlling your keyboard and mouse programmatically.

![image](https://github.com/user-attachments/assets/be73c066-0ddf-4b0b-9124-c6f1e6a75df0)





**Keyboard detection steps:**

✅ Step 1 – Installed Required Libraries

    pip install opencv-python mediapipe pyautogui keyboard

✅ Step 2 – Created a Python Script to Open the Camera

      camera_test.py

✅ Step 3 – Created a Python Script to Detect Hands 

      mediapipe_test.py

✅ Step 4 – Use Hand Landmarks to Detect Left or Right Movement

   Use the position of my hands to decide if I’m turning left, right, or center — so later we can control steering in the game.

      turning_test.py

✅ Step 5 – Use Hand Landmarks to Detect Acc or Brake Movement

   Use the distance between tip of the middle finger (landmark 12) and the wrist (landmark 0)

      acc_test.py

✅ Step 6 – Simulate turning keys pressing

   Use pynput to simuates virtual pressing keys

      turn_key.py

✅ Step 6 – Simulate acc/brake keys pressing

      acc_key.py

✅ Step 7 – Final key detector main script

      main.py

Thanks for checking out this project! Controlling the keyboard with hand detection is just the beginning, there’s so much potential to explore in gesture-based interfaces. Feel free to try it out, experiment with it, and see what you can build on top of it. If you have ideas for improvements, want to collaborate, or just have questions, don’t hesitate to reach out. Let’s connect and make it even better together!


