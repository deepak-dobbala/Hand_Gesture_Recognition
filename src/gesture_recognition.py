import math

class GestureRecognizer:
    def __init__(self):
        self.gestures = {
            'click': self.detect_click,
            'move': self.detect_move,
            'right_click': self.detect_right_click
        }

    def detect_click(self, landmarks):
        # Get index finger tip (landmark 8) and middle finger tip (landmark 12)
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        
        # Calculate distance between index and middle finger tips
        distance = math.sqrt((middle_tip[1] - index_tip[1])**2 + (middle_tip[2] - index_tip[2])**2)
        
        # You may need to adjust this threshold based on your camera and setup
        return distance < 50  # Smaller threshold since fingers are closer together

    def detect_move(self, landmarks):
        # Implement logic to detect hand movement
        # This could be based on the position of a specific landmark (e.g., index finger tip)
        return True  # For now, always return True to enable mouse movement

    def detect_right_click(self, landmarks):
        # Ring and middle finger pinch
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        
        # Calculate distance between middle and ring finger tips
        distance = math.sqrt((ring_tip[1] - middle_tip[1])**2 + (ring_tip[2] - middle_tip[2])**2)
        
        # You may need to adjust this threshold based on your camera and setup
        return distance < 50  # Similar threshold to regular click

    def recognize_gesture(self, landmarks):
        recognized_gestures = []
        for gesture, detect_func in self.gestures.items():
            if detect_func(landmarks):
                recognized_gestures.append(gesture)
        return recognized_gestures