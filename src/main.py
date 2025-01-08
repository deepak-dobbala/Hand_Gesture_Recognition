import cv2
import numpy as np
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer
from mouse_control import MouseController

class MovementSmoother:
    def __init__(self, smoothing_factor=0.5, stability_threshold=0.01):
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing_factor = smoothing_factor
        self.stability_threshold = stability_threshold

    def smooth(self, x, y):
        # If this is the first movement, initialize previous positions
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y
            return x, y

        # Calculate change in position
        delta_x = abs(x - self.prev_x)
        delta_y = abs(y - self.prev_y)

        # If movement is very small, ignore it to prevent jitter
        if delta_x < self.stability_threshold and delta_y < self.stability_threshold:
            return self.prev_x, self.prev_y

        # Apply exponential moving average
        smoothed_x = self.prev_x + self.smoothing_factor * (x - self.prev_x)
        smoothed_y = self.prev_y + self.smoothing_factor * (y - self.prev_y)

        # Update previous positions
        self.prev_x, self.prev_y = smoothed_x, smoothed_y

        return smoothed_x, smoothed_y

def calculate_palm_center(landmarks):
    """Calculate the center of the palm using key landmarks"""
    # Use wrist (0) and knuckle points (5,9,13,17) to find palm center
    wrist = landmarks[0]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]
    
    # Calculate average position
    x = (wrist[1] + index_mcp[1] + middle_mcp[1] + ring_mcp[1] + pinky_mcp[1]) / 5
    y = (wrist[2] + index_mcp[2] + middle_mcp[2] + ring_mcp[2] + pinky_mcp[2]) / 5
    
    return int(x), int(y)

def main():
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()
    movement_smoother = MovementSmoother(smoothing_factor=0.3, stability_threshold=0.005)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Mirror the image
        
        img = hand_tracker.find_hands(img)
        landmarks = hand_tracker.find_position(img)
        
        if landmarks:
            # Calculate palm center
            palm_x, palm_y = calculate_palm_center(landmarks)
            
            # Normalize coordinates
            x = palm_x / img.shape[1]
            y = palm_y / img.shape[0]
            
            # Apply smoothing to the coordinates
            smoothed_x, smoothed_y = movement_smoother.smooth(x, y)
            
            # Draw the control point on the image (optional)
            cv2.circle(img, (palm_x, palm_y), 8, (0, 0, 255), cv2.FILLED)
            
            # Recognize gestures
            gestures = gesture_recognizer.recognize_gesture(landmarks)
            
            # Control the mouse
            if 'move' in gestures:
                mouse_controller.move(smoothed_x, smoothed_y)
            if 'click' in gestures:
                mouse_controller.click()
            if 'right_click' in gestures:
                mouse_controller.right_click()
            if 'terminate' in gestures:
                break  # Exit the program when terminate gesture is detected
        
        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
