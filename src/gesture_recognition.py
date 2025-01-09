import math

class GestureRecognizer:
    def __init__(self):
        self.gestures = {
            'click': self.detect_click,
            'move': self.detect_move,
            'right_click': self.detect_right_click,
            'terminate': self.detect_terminate,
            'scroll': self.detect_scroll,
            'zoom': self.detect_zoom
        }
        self.scroll_active = False
        self.scroll_direction = None
        self.prev_zoom_distance = None

    def are_main_fingers_open(self, landmarks):
        """Check if thumb, index, and middle fingers are open while others are closed"""
        # Get base positions
        thumb_base = landmarks[2]
        index_base = landmarks[5]
        middle_base = landmarks[9]
        
        # Get tip positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Check if main fingers are extended (tip above base)
        thumb_open = thumb_tip[2] < thumb_base[2]
        index_open = index_tip[2] < index_base[2]
        middle_open = middle_tip[2] < middle_base[2]
        
        # Check if other fingers are closed
        ring_closed = ring_tip[2] > landmarks[13][2]
        pinky_closed = pinky_tip[2] > landmarks[17][2]
        
        return thumb_open and index_open and middle_open and ring_closed and pinky_closed

    def detect_click(self, landmarks):
        """Detect left click: thumb tip to index PIP (middle joint)"""
        thumb_tip = landmarks[4]
        index_pip = landmarks[6]  # Index finger PIP joint
        
        # Calculate distance
        distance = math.sqrt((thumb_tip[1] - index_pip[1])**2 + (thumb_tip[2] - index_pip[2])**2)
        
        # Increase threshold slightly and add some buffer
        return distance < 45  # Adjusted threshold for easier detection

    def detect_right_click(self, landmarks):
        """Detect right click: index tip to middle tip"""
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        
        # Calculate distance
        distance = math.sqrt((middle_tip[1] - index_tip[1])**2 + (middle_tip[2] - index_tip[2])**2)
        
        # Increase threshold slightly
        return distance < 45  # Adjusted threshold for easier detection

    def detect_terminate(self, landmarks):
        if not self.are_main_fingers_open(landmarks):
            return False
            
        # Detect termination when thumb tip gets close to middle tip
        thumb_tip = landmarks[4]
        middle_tip = landmarks[12]
        
        distance = math.sqrt((middle_tip[1] - thumb_tip[1])**2 + (middle_tip[2] - thumb_tip[2])**2)
        return distance < 70

    def detect_move(self, landmarks):
        # Allow movement at any time as long as hand is detected
        return True

    def detect_scroll(self, landmarks):
        """
        Detect scroll gesture:
        - Main three fingers must be open (thumb, index, middle)
        - Index-thumb close = scroll up
        - Index-middle close = scroll down
        """
        # Get finger positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Get base positions
        thumb_base = landmarks[2]
        index_base = landmarks[5]
        middle_base = landmarks[9]
        ring_base = landmarks[13]
        pinky_base = landmarks[17]
        
        # Check if main three fingers are open and others closed
        main_fingers_open = (
            thumb_tip[2] < thumb_base[2] and   # thumb open
            index_tip[2] < index_base[2] and   # index open
            middle_tip[2] < middle_base[2]      # middle open
        )
        others_closed = (
            ring_tip[2] > ring_base[2] and     # ring closed
            pinky_tip[2] > pinky_base[2]       # pinky closed
        )
        
        if not (main_fingers_open and others_closed):
            self.scroll_active = False
            self.scroll_direction = None
            return False, 0
            
        # Calculate distances
        thumb_index_distance = math.sqrt(
            (thumb_tip[1] - index_tip[1])**2 + 
            (thumb_tip[2] - index_tip[2])**2
        )
        index_middle_distance = math.sqrt(
            (middle_tip[1] - index_tip[1])**2 + 
            (middle_tip[2] - index_tip[2])**2
        )
        
        # Check for scroll up (thumb-index pinch)
        if thumb_index_distance < 40:
            self.scroll_active = True
            self.scroll_direction = 'up'
            return True, 5  # Positive value for scroll up
            
        # Check for scroll down (index-middle pinch)
        if index_middle_distance < 40:
            self.scroll_active = True
            self.scroll_direction = 'down'
            return True, -5  # Negative value for scroll down
            
        self.scroll_active = False
        self.scroll_direction = None
        return False, 0

    def detect_zoom(self, landmarks):
        """
        Detect zoom gesture:
        - Only thumb and pinky extended
        - Other fingers closed
        - Zoom based on distance between thumb and pinky tips
        """
        # Get finger positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Get base positions
        thumb_base = landmarks[2]
        index_base = landmarks[5]
        middle_base = landmarks[9]
        ring_base = landmarks[13]
        pinky_base = landmarks[17]
        
        # Check if only thumb and pinky are extended
        thumb_pinky_extended = (
            thumb_tip[2] < thumb_base[2] and   # thumb extended
            pinky_tip[2] < pinky_base[2]       # pinky extended
        )
        
        others_closed = (
            index_tip[2] > index_base[2] and   # index closed
            middle_tip[2] > middle_base[2] and  # middle closed
            ring_tip[2] > ring_base[2]         # ring closed
        )
        
        if thumb_pinky_extended and others_closed:
            # Calculate distance between thumb and pinky tips
            distance = math.sqrt(
                (thumb_tip[1] - pinky_tip[1])**2 + 
                (thumb_tip[2] - pinky_tip[2])**2
            )
            
            # Draw line between thumb and pinky for visual feedback
            return True, distance, (thumb_tip[1], thumb_tip[2]), (pinky_tip[1], pinky_tip[2])
            
        self.prev_zoom_distance = None
        return False, 0, None, None

    def recognize_gesture(self, landmarks):
        # First check for termination gesture
        if self.detect_terminate(landmarks):
            self.scroll_active = False
            self.scroll_direction = None
            self.prev_zoom_distance = None
            return ['terminate']
        
        # Check for zoom gesture
        is_zooming, zoom_distance, thumb_tip, pinky_tip = self.detect_zoom(landmarks)
        if is_zooming:
            return ['zoom', zoom_distance, thumb_tip, pinky_tip]
        
        # Check for scroll gesture
        is_scrolling, scroll_amount = self.detect_scroll(landmarks)
        if is_scrolling:
            return ['scroll', scroll_amount]
        
        # Only check for other gestures if not zooming or scrolling
        recognized_gestures = []
        for gesture, detect_func in self.gestures.items():
            if gesture not in ['terminate', 'scroll', 'zoom'] and detect_func(landmarks):
                recognized_gestures.append(gesture)
        
        return recognized_gestures
