import pyautogui
import time

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False
        self.base_zoom_distance = None

    def move(self, x, y):
        # Convert the coordinates to screen coordinates
        screen_x = int(x * self.screen_width)
        screen_y = int(y * self.screen_height)
        pyautogui.moveTo(screen_x, screen_y)

    def click(self):
        pyautogui.click()
        time.sleep(0.2)  # Add delay to prevent multiple clicks

    def double_click(self):
        """Perform a double click"""
        pyautogui.doubleClick()

    def right_click(self):
        pyautogui.rightClick()
        time.sleep(0.2)  # Add delay to prevent multiple clicks

    def zoom(self, distance):
        """
        Handle zoom based on thumb-pinky distance
        Larger distance = zoom in
        Smaller distance = zoom out
        """
        if self.base_zoom_distance is None:
            self.base_zoom_distance = distance
            return
        
        # Calculate zoom factor based on change in distance
        zoom_factor = (distance - self.base_zoom_distance) / self.base_zoom_distance
        
        # Convert to scroll units and apply zoom
        scroll_amount = int(zoom_factor * 20)  # Increased multiplier for more noticeable zoom
        
        if abs(scroll_amount) > 0:  # Only zoom if there's significant change
            # Make sure ctrl is pressed and released properly
            pyautogui.keyDown('ctrl')
            # Use larger scroll steps for more noticeable zoom
            if scroll_amount > 0:
                pyautogui.scroll(2)  # Zoom in
            else:
                pyautogui.scroll(-2)  # Zoom out
            pyautogui.keyUp('ctrl')
            
            # Update base distance for next calculation
            self.base_zoom_distance = distance
            
            # Add small delay to prevent too rapid zooming
            time.sleep(0.05)
    
    def reset_zoom(self):
        """Reset zoom tracking"""
        self.base_zoom_distance = None

    def scroll(self, amount):
        """
        Scroll based on amount
        Positive amount = scroll up
        Negative amount = scroll down
        """
        if abs(amount) > 0.5:  # Threshold to prevent tiny scrolls
            scroll_steps = int(amount * 5)  # Adjust multiplier for scroll sensitivity
            pyautogui.scroll(scroll_steps)

    def minimize_window(self):
        """Minimize the active window"""
        pyautogui.hotkey('win', 'down')  # Windows shortcut to minimize

    def start_selection(self):
        """Start mass selection by holding down left mouse button"""
        pyautogui.mouseDown()
    
    def end_selection(self):
        """End mass selection by releasing left mouse button"""
        pyautogui.mouseUp()

    def start_drag(self):
        """Start dragging by holding down left mouse button"""
        pyautogui.mouseDown()
    
    def end_drag(self):
        """End dragging by releasing left mouse button"""
        pyautogui.mouseUp()
