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

4. pynput ⌨️

     A Python library for controlling your keyboard and mouse programmatically.

![image](https://github.com/user-attachments/assets/be73c066-0ddf-4b0b-9124-c6f1e6a75df0)

6. FastAPI 🚀

     A modern, fast (high-performance) Python web framework for building APIs
     Supports WebSockets for real-time communication between your React frontend and Python backend

5. React ⚛️

     A popular JavaScript library for building user interfaces
     Enables seamless integration of webcam video capture in the browser
     Can send webcam frames or processed data to the backend via WebSockets or HTTP



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

      key_detect.py



**backend steps:**

✅ Step 1 – Installed Required Libraries

    pip install fastapi uvicorn python-multipart aiofiles


✅ Step 2 – Virtual environment(venv)

   Install and use a virtual environment (venv) to keep all the project’s Python packages separate and organized, and ensure the project runs smoothly and consistently on any machine.

   create env:    

            python3 -m venv venv
   activate:

            source venv/bin/activate
   run fastapi app:

            uvicorn test:app --reload

✅ Step 3 – Install the backend dependencies

      pip install -r requirements.txt


**frontend steps:**

✅ Step 1 – Set React App

      cd frontend
      npm create vite@latest
      npm install && npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion


   
