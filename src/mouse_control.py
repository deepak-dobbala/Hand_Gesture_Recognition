import pyautogui

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

    def double_click(self):
        pyautogui.doubleClick()

    def right_click(self):
        pyautogui.rightClick()

    def zoom(self, distance):
        if self.base_zoom_distance is None:
            self.base_zoom_distance = distance
            return
        
        zoom_factor = (distance - self.base_zoom_distance) / self.base_zoom_distance
        scroll_amount = int(zoom_factor * 10)
        if scroll_amount != 0:
            pyautogui.scroll(scroll_amount)
            self.base_zoom_distance = distance
    
    def reset_zoom(self):
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
