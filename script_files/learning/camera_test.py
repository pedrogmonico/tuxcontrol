import cv2  # Import the OpenCV library

# Start the webcam (0 means default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame from the webcam
    success, frame = cap.read()

    # Show the frame in a window
    cv2.imshow("Webcam", frame)

    # Press 'q' to quit the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

"""
This Python script uses the OpenCV (cv2) library to create a simple real-time webcam viewer. It starts by connecting to the default camera (usually your laptop’s built-in webcam) using cv2.VideoCapture(0). The webcam stream is then read frame-by-frame inside a continuous while loop. For each loop iteration, a new video frame is captured and displayed in a window titled "Webcam" using cv2.imshow().
"""