import math

class GestureRecognizer:
    def __init__(self):
        self.gestures = {
            'click': self.detect_click,
            'move': self.detect_move
        }

    def detect_click(self, landmarks):
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = math.sqrt((thumb_tip[1] - index_tip[1])**2 + (thumb_tip[2] - index_tip[2])**2)
        
        return distance < 40  # You may need to adjust this threshold

    def detect_move(self, landmarks):
        # Implement logic to detect hand movement
        # This could be based on the position of a specific landmark (e.g., index finger tip)
        return True  # For now, always return True to enable mouse movement

    def recognize_gesture(self, landmarks):
        recognized_gestures = []
        for gesture, detect_func in self.gestures.items():
            if detect_func(landmarks):
                recognized_gestures.append(gesture)
        return recognized_gestures