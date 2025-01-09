import cv2
import numpy as np
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer
from mouse_control import MouseController
import time

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
    # Initialize camera with optimized settings
    cap = cv2.VideoCapture(0)
    
    # Set camera properties for higher FPS
    cap.set(cv2.CAP_PROP_FPS, 60)  # Request 60 FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduce resolution height
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Use MJPG codec
    
    # Optional: Print actual FPS to verify settings
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Camera FPS: {actual_fps}")
    
    hand_tracker = HandTracker(
        static_image_mode=False,  # Set to False for better performance
        max_num_hands=1,  # Limit to one hand for better performance
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()
    movement_smoother = MovementSmoother(smoothing_factor=0.3, stability_threshold=0.005)

    # FPS calculation variables
    prev_time = 0
    curr_time = 0
    
    while True:
        success, img = cap.read()
        
        # Calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        # Display FPS
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        img = cv2.flip(img, 1)
        
        img = hand_tracker.find_hands(img)
        landmarks = hand_tracker.find_position(img)
        
        if landmarks:
            palm_x, palm_y = calculate_palm_center(landmarks)
            x = palm_x / img.shape[1]
            y = palm_y / img.shape[0]
            smoothed_x, smoothed_y = movement_smoother.smooth(x, y)
            cv2.circle(img, (palm_x, palm_y), 8, (0, 0, 255), cv2.FILLED)
            
            # Recognize gestures
            gestures = gesture_recognizer.recognize_gesture(landmarks)
            
            # Draw visual feedback for gestures
            if landmarks:
                # Draw palm center
                cv2.circle(img, (palm_x, palm_y), 8, (0, 0, 255), cv2.FILLED)
                
                # Draw click points
                thumb_tip = (landmarks[4][1], landmarks[4][2])
                index_pip = (landmarks[6][1], landmarks[6][2])
                index_tip = (landmarks[8][1], landmarks[8][2])
                middle_tip = (landmarks[12][1], landmarks[12][2])
                
                # Draw points for left click
                cv2.circle(img, (int(thumb_tip[0]), int(thumb_tip[1])), 5, (255, 0, 0), -1)
                cv2.circle(img, (int(index_pip[0]), int(index_pip[1])), 5, (255, 0, 0), -1)
                
                # Draw points for right click
                cv2.circle(img, (int(index_tip[0]), int(index_tip[1])), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(middle_tip[0]), int(middle_tip[1])), 5, (0, 255, 0), -1)
            
            # Handle gestures
            if isinstance(gestures, list) and len(gestures) > 1:
                if gestures[0] == 'scroll':
                    mouse_controller.scroll(gestures[1])
                elif gestures[0] == 'zoom':
                    zoom_distance = gestures[1]
                    # Draw line between thumb and pinky for zoom
                    if len(gestures) > 2:
                        p1, p2 = gestures[2], gestures[3]
                        cv2.line(img, (int(p1[0]), int(p1[1])), 
                                (int(p2[0]), int(p2[1])), (0, 255, 255), 2)
                    mouse_controller.zoom(zoom_distance)
            
            # Handle click gestures with priority
            if 'click' in gestures:
                mouse_controller.click()
                # Add small delay to prevent multiple clicks
                time.sleep(0.1)
            elif 'right_click' in gestures:
                mouse_controller.right_click()
                # Add small delay to prevent multiple clicks
                time.sleep(0.1)
            elif 'move' in gestures:
                mouse_controller.move(smoothed_x, smoothed_y)
            
            if 'terminate' in gestures:
                break
        
        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
