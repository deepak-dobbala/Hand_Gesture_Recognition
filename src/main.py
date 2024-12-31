import cv2
import numpy as np
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer
from mouse_control import MouseController

def main():
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Mirror the image
        
        img = hand_tracker.find_hands(img)
        landmarks = hand_tracker.find_position(img)
        
        if landmarks:
            # Get the tip of the index finger
            index_finger_tip = landmarks[8]
            
            # Normalize coordinates
            x = index_finger_tip[1] / img.shape[1]
            y = index_finger_tip[2] / img.shape[0]
            
            # Recognize gestures
            gestures = gesture_recognizer.recognize_gesture(landmarks)
            
            # Control the mouse
            if 'move' in gestures:
                mouse_controller.move(x, y)
            if 'click' in gestures:
                mouse_controller.click()
        
        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()