import math

class GestureRecognizer:
    def __init__(self):
        self.gestures = {
            'click': self.detect_click,
            'move': self.detect_move,
            'right_click': self.detect_right_click,
            'terminate': self.detect_terminate
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
        # Check if we have enough landmarks to detect palm
        if len(landmarks) >= 9:  # We need at least up to landmark 9 for palm detection
            return True
        return False

    def detect_right_click(self, landmarks):
        # Ring and middle finger pinch
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        
        # Calculate distance between middle and ring finger tips
        distance = math.sqrt((ring_tip[1] - middle_tip[1])**2 + (ring_tip[2] - middle_tip[2])**2)
        
        # You may need to adjust this threshold based on your camera and setup
        return distance < 50  # Similar threshold to regular click

    def detect_terminate(self, landmarks):
        # Get thumb tip and middle finger tip
        thumb_tip = landmarks[4]
        middle_tip = landmarks[12]
        
        # Calculate distance between thumb and middle finger tips
        distance = math.sqrt((middle_tip[1] - thumb_tip[1])**2 + (middle_tip[2] - thumb_tip[2])**2)
        
        # Return true if thumb and middle finger are close
        return distance < 70  # Increased threshold to detect termination earlier      

    def recognize_gesture(self, landmarks):
        recognized_gestures = []
        
        # First check for termination gesture
        if self.detect_terminate(landmarks):
            return ['terminate']  # Return only terminate gesture
        
        # If not terminating, check for other gestures
        for gesture, detect_func in self.gestures.items():
            if gesture != 'terminate' and detect_func(landmarks):  # Skip terminate check as it's done above
                recognized_gestures.append(gesture)
        
        return recognized_gestures
